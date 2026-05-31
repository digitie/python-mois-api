"""file.localdata.go.kr 생활편의정보 추가 slug 탐색 스크립트.

현재 카탈로그에 없는 생활편의정보 slug 후보를 HTTP로 프로브해
존재 여부를 확인한다. 403은 "인증 필요(slug 존재 가능성 있음)",
404는 "slug 없음"으로 해석한다.

사용법:
    python tools/probe_life_convenience.py

서비스키가 없어도 동작한다. info 페이지(인증 불필요)를 기준으로
slug 존재 여부만 확인한다.
"""

from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mois.catalog import FILE_DOWNLOADS  # noqa: E402

BASE_URL = "https://file.localdata.go.kr"
REFERER = BASE_URL

KNOWN_SLUGS = {r["slug"] for r in FILE_DOWNLOADS if r["kind"] == "life_convenience"}

# 탐색 후보: (slug, 설명)
CANDIDATES: list[tuple[str, str]] = [
    # 교통/이동
    ("parking_lot_info", "공영주차장정보"),
    ("public_bicycle_info", "공공자전거(따릉이류)정보"),
    ("bus_stop_info", "버스정류장정보"),
    ("subway_station_info", "지하철역정보"),
    # 안전/보건
    ("aed_info", "자동심장충격기(AED)정보"),
    ("fire_hydrant_info", "소화전정보"),
    ("outdoor_cctv_info", "야외CCTV정보"),
    # 복지/생활
    ("public_library_info", "공공도서관정보"),
    ("small_library_info", "작은도서관정보"),
    ("child_care_center_info", "어린이집정보"),
    ("child_playground_info", "어린이놀이터정보"),
    ("senior_welfare_center_info", "노인복지관정보"),
    ("welfare_facility_info", "복지시설정보"),
    ("disability_welfare_facility_info", "장애인복지시설정보"),
    # 환경/에너지
    ("recycling_center_info", "재활용센터정보"),
    ("ev_charger_info", "전기차충전소정보"),
    ("solar_facility_info", "태양광발전시설정보"),
    # 공공시설
    ("public_sports_facility_info", "공공체육시설정보"),
    ("outdoor_exercise_facility_info", "야외운동시설정보"),
    ("public_park_info", "공원정보"),
    ("drinking_fountain_info", "음수대정보"),
    ("street_tree_info", "가로수정보"),
    # 재난/안전
    ("disaster_shelter_info", "재난대피소정보"),
    ("flood_shelter_info", "침수대피소정보"),
    # 기타 공공
    ("public_toilet_for_disabled_info", "장애인화장실정보"),
    ("salt_production_info", "천일염생산시설정보"),
    ("sharing_economy_info", "공유경제정보"),
    ("village_hall_info", "마을회관정보"),
]


def probe(slug: str) -> int:
    """HTTP GET → 상태코드 반환. 네트워크 오류는 -1.

    상태코드 해석:
    - 200: slug 존재, 안내 페이지 접근 가능 → catalog.py 추가 대상
    - 403: slug 존재하지만 인증 필요 → 존재 가능성 있음
    - 500: Spring Boot Whitelabel Error (경로 미매핑) → slug 없음
    - 404: 명시적 404 → slug 없음
    """
    url = f"{BASE_URL}/file/{slug}/info"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": REFERER,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1


def main() -> None:
    print(f"현재 카탈로그 생활편의정보: {sorted(KNOWN_SLUGS)}\n")
    print(f"탐색 후보: {len(CANDIDATES)}개\n")
    print("상태코드 기준: 200=존재, 403=인증필요(존재 가능), 500/404=없음\n")

    results: dict[str, tuple[int, str]] = {}
    for slug, desc in CANDIDATES:
        if slug in KNOWN_SLUGS:
            print(f"  SKIP  {slug} ({desc}) -- 이미 카탈로그에 있음")
            continue
        status = probe(slug)
        results[slug] = (status, desc)
        marker = "OK" if status == 200 else ("?" if status == 403 else "X")
        print(f"  [{status:3d}] {marker} {slug} ({desc})")
        time.sleep(0.3)

    print("\n=== 결과 요약 ===")
    found = [(s, d) for s, (c, d) in results.items() if c == 200]
    maybe = [(s, d) for s, (c, d) in results.items() if c == 403]
    absent = [(s, d) for s, (c, d) in results.items() if c not in (200, 403)]

    if found:
        print(f"\n[200 접근 가능] {len(found)}개 -- catalog.py에 추가 권장:")
        for s, d in found:
            print(f"  {s}  # {d}")

    if maybe:
        print(f"\n[403 인증 필요] {len(maybe)}개 -- slug 존재 가능성 있음:")
        for s, d in maybe:
            print(f"  {s}  # {d}")

    if absent:
        print(f"\n[없음] {len(absent)}개 (500/404 등):")
        for s, d in absent:
            print(f"  {s}  # {d}")

    if not found and not maybe:
        print("\n현재 file.localdata.go.kr에 추가 생활편의정보 slug가 없습니다.")
        print("서비스 갱신 후 재실행하거나 후보 slug 목록을 추가해 재탐색하세요.")


if __name__ == "__main__":
    main()
