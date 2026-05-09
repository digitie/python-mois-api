"""다운로드된 localdata 파일을 DB 브라우저용 PostGIS 테이블에 적재하는 CLI."""

from __future__ import annotations

import argparse
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, func, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from pymois import (
    LocalDataRecord,
    PlaceDetail,
    PlaceMaster,
    PlaceRecord,
    create_postgis_schema,
    record_to_place_record,
)
from pymois.db import place_detail_values, place_master_values
from pymois.files import iter_records_from_binary


def load_download_file_to_postgis(
    *,
    database_url: str,
    file_path: str | os.PathLike[str],
    slug: str,
    batch_size: int = 1000,
    replace_slug: bool = False,
    create_extension: bool = True,
) -> int:
    """다운로드된 CSV/ZIP 파일 하나를 PostGIS DB에 적재합니다."""

    engine = create_engine(database_url, pool_pre_ping=True)
    create_postgis_schema(engine, create_extension=create_extension)
    if replace_slug:
        delete_slug(engine, slug)

    with Path(file_path).open("rb") as source, Session(engine) as session:
        return load_records_to_postgis(
            session,
            iter_records_from_binary(source, slug=slug),
            batch_size=batch_size,
        )


def load_records_to_postgis(
    session: Session,
    records: Iterable[LocalDataRecord],
    *,
    batch_size: int = 1000,
) -> int:
    """레코드 스트림을 배치 UPSERT하고 배치 단위로 커밋합니다."""

    if batch_size < 1:
        raise ValueError("batch_size must be greater than 0")

    count = 0
    batch: list[LocalDataRecord] = []
    for record in records:
        batch.append(record)
        count += 1
        if len(batch) >= batch_size:
            _bulk_upsert_places(session, batch)
            session.commit()
            batch = []

    if batch:
        _bulk_upsert_places(session, batch)
        session.commit()
    return count


def delete_slug(engine: Engine, slug: str) -> None:
    """재적재 전 특정 업종의 기존 마스터/상세 데이터를 삭제합니다."""

    with engine.begin() as connection:
        connection.execute(
            text("delete from mois_place_master where service_slug = :slug"),
            {"slug": slug},
        )


def _bulk_upsert_places(session: Session, records: list[LocalDataRecord]) -> None:
    places = [record_to_place_record(record) for record in records]
    deduped_places = _dedupe_places(places)
    if not deduped_places:
        return

    master_rows = [place_master_values(place) for place in deduped_places]
    master_insert = insert(PlaceMaster).values(master_rows)
    master_update_values = _excluded_update_values(
        master_insert,
        master_rows[0],
        skip={"place_id", "service_slug", "mng_no"},
    )
    master_update_values["updated_at"] = func.now()
    master_statement = (
        master_insert.on_conflict_do_update(
            constraint="uq_mois_place_master_source",
            set_=master_update_values,
        )
        .returning(PlaceMaster.service_slug, PlaceMaster.mng_no, PlaceMaster.place_id)
    )
    place_ids = {
        (str(row.service_slug), str(row.mng_no)): row.place_id
        for row in session.execute(master_statement)
    }

    detail_rows = [
        place_detail_values(place, place_ids[(place.service_slug, place.mng_no or "")])
        for place in deduped_places
    ]
    detail_insert = insert(PlaceDetail).values(detail_rows)
    detail_update_values = _excluded_update_values(
        detail_insert,
        detail_rows[0],
        skip={"place_id"},
    )
    detail_update_values["updated_at"] = func.now()
    session.execute(
        detail_insert.on_conflict_do_update(
            index_elements=[PlaceDetail.place_id],
            set_=detail_update_values,
        )
    )


def _dedupe_places(places: Iterable[PlaceRecord]) -> list[PlaceRecord]:
    deduped: dict[tuple[str, str], PlaceRecord] = {}
    for place in places:
        deduped[(place.service_slug, place.mng_no or "")] = place
    return list(deduped.values())


def _excluded_update_values(
    insert_statement: Any,
    values: dict[str, Any],
    *,
    skip: set[str],
) -> dict[str, Any]:
    return {
        key: getattr(insert_statement.excluded, key)
        for key in values
        if key not in skip
    }


def main() -> None:
    """명령행 진입점."""

    parser = argparse.ArgumentParser(
        description="다운로드된 localdata CSV/ZIP 파일을 pymois PostGIS 테이블에 적재합니다.",
    )
    parser.add_argument("--file", required=True, help="다운로드된 CSV/ZIP 파일 경로")
    parser.add_argument("--slug", required=True, help="파일 카탈로그 slug")
    parser.add_argument(
        "--database-url",
        default=os.getenv("MOIS_DATABASE_URL"),
        help="SQLAlchemy DB URL. 기본값은 MOIS_DATABASE_URL 환경변수입니다.",
    )
    parser.add_argument("--batch-size", type=int, default=1000, help="커밋 배치 크기")
    parser.add_argument("--replace-slug", action="store_true", help="같은 slug 데이터를 먼저 삭제")
    parser.add_argument(
        "--skip-create-extension",
        action="store_true",
        help="PostGIS 확장 생성 권한이 없을 때 사용",
    )
    args = parser.parse_args()

    if not args.database_url:
        parser.error("--database-url 또는 MOIS_DATABASE_URL이 필요합니다")

    count = load_download_file_to_postgis(
        database_url=args.database_url,
        file_path=args.file,
        slug=args.slug,
        batch_size=args.batch_size,
        replace_slug=args.replace_slug,
        create_extension=not args.skip_create_extension,
    )
    print(f"loaded={count} slug={args.slug} file={args.file}")


if __name__ == "__main__":
    main()
