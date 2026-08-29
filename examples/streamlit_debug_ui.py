"""Streamlit 기반 mois 지방행정 인허가정보 OpenAPI 디버그 카탈로그 뷰어."""
# ruff: noqa: E402

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
for module_name, module in list(sys.modules.items()):
    if module_name != "mois" and not module_name.startswith("mois."):
        continue
    module_file = getattr(module, "__file__", None)
    if module_file is not None and not Path(module_file).resolve().is_relative_to(SRC):
        del sys.modules[module_name]

try:
    import pandas as pd
    import streamlit as st
except ModuleNotFoundError as exc:  # pragma: no cover - 선택 실행 도구
    raise SystemExit('Streamlit UI를 쓰려면 `pip install -e ".[debug-ui]"`를 실행하세요.') from exc

from mois import (
    ConditionOperator,
    DebugRun,
    MoisClient,
    OpenApiKind,
    error_to_dict,
    get_api_catalog,
    jsonable,
    redact_sensitive,
    save_fixture,
)

CONDITION_ROW_COUNT = 3
DEFAULT_FIXTURE_DIR = ROOT / "tests" / "fixtures"


def main() -> None:
    st.set_page_config(page_title="mois OpenAPI Debug", layout="wide")
    st.title("mois OpenAPI Debug")

    rows = list(get_api_catalog())
    sources = sorted({row["data_source"] for row in rows})
    source = st.sidebar.selectbox("Data source", sources)
    source_rows = [row for row in rows if row["data_source"] == source]

    categories = sorted({row["category"] for row in source_rows})
    category = st.sidebar.selectbox("Category", categories)
    category_rows = [row for row in source_rows if row["category"] == category]

    labels = [row["dataset_label"] for row in category_rows]
    selected_label = st.sidebar.selectbox("API", labels)
    selected = category_rows[labels.index(selected_label)]

    st.sidebar.caption(_api_summary_line(selected))
    st.sidebar.caption(_api_response_line(selected))

    env_names = tuple(str(name) for name in selected["service_key_env_names"])
    env_value = _env_key_value(env_names)

    st.sidebar.subheader("Environment")
    environment = st.sidebar.radio(
        "Environment",
        ["env", "manual"],
        index=0 if env_value else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    if environment == "env":
        if env_value:
            st.sidebar.caption(f"{env_names[0]} 값을 사용합니다.")
        else:
            st.sidebar.caption(f"{env_names[0]}가 설정되어 있지 않습니다. manual로 전환하세요.")
    else:
        st.sidebar.caption("아래 Auth 입력창의 수동 값을 사용합니다.")

    st.sidebar.subheader("Auth")
    if environment == "manual":
        effective_service_key = st.sidebar.text_input(
            "serviceKey",
            value="",
            type="password",
            placeholder="공공데이터포털 서비스키(인코딩 전 값)",
            help=f"사용 가능한 env 이름: {', '.join(env_names)}",
        )
    else:
        effective_service_key = env_value or ""

    st.sidebar.link_button("서비스키 발급/확인", selected["service_key_url"])

    timeout = st.sidebar.number_input(
        "Timeout",
        min_value=1.0,
        max_value=60.0,
        value=10.0,
        step=1.0,
        help="API 요청 timeout seconds입니다.",
    )

    fixture_base_dir = _fixture_base_dir_sidebar()

    tabs = st.tabs(
        [
            "Raw Response",
            "Pydantic Model",
            "Processed Result",
            "Validation Errors",
            "Debug Trace",
            "Fixture / Testcase",
        ]
    )

    with tabs[0]:
        _raw_response_tab(selected, effective_service_key, timeout=float(timeout))
    with tabs[1]:
        _pydantic_model_tab(selected)
    with tabs[2]:
        _processed_result_tab(selected)
    with tabs[3]:
        _validation_errors_tab(selected)
    with tabs[4]:
        _debug_trace_tab(selected, env_names)
    with tabs[5]:
        _fixture_tab(fixture_base_dir, selected)


def _raw_response_tab(selected: dict[str, Any], service_key: str, *, timeout: float) -> None:
    st.subheader(selected["dataset_name"])
    st.caption(f"{selected['data_source']} / {selected['category']} / {selected['service_key']}")

    try:
        submitted, params, request_options, missing = _request_form(selected)
    except ValueError as exc:
        st.error(str(exc))
        st.json(redact_sensitive(jsonable(error_to_dict(exc))))
        return

    preview = {
        **params,
        "conditions": {
            field: {"operator": operator, "value": value}
            for field, (operator, value) in request_options["conditions"].items()
        },
        "kind": request_options["kind"],
        "pageNo": request_options["page_no"],
        "numOfRows": request_options["num_of_rows"],
    }
    st.subheader("Request params preview")
    st.json(preview)

    if not submitted:
        return
    if missing:
        st.error("필수 파라미터를 입력하세요: " + ", ".join(missing))
        return

    run = _execute_debug_request(
        selected,
        service_key,
        timeout=timeout,
        params=params,
        conditions=request_options["conditions"],
        kind=request_options["kind"],
        page_no=request_options["page_no"],
        num_of_rows=request_options["num_of_rows"],
    )
    _store_run(selected, request_options["kind"], run)

    if run.error:
        st.error(run.error.get("message", "실행 중 오류가 발생했습니다."))
    st.json(jsonable(run.response))


def _request_form(
    selected: dict[str, Any],
) -> tuple[bool, dict[str, Any], dict[str, Any], list[str]]:
    required_names = tuple(str(name) for name in selected["required_params"])
    optional_names = tuple(str(name) for name in selected["optional_params"])
    key_prefix = f"{selected['data_source']}:{selected['service_key']}"

    with st.form(f"request-form:{key_prefix}"):
        st.subheader("Required parameters")
        if required_names:
            required_values = _render_text_grid(required_names, key_prefix=f"{key_prefix}:required")
        else:
            st.caption(
                "이 API에는 필수 쿼리 파라미터가 없습니다"
                "(serviceKey/pageNo/numOfRows는 자동으로 채워집니다)."
            )
            required_values = {}

        st.subheader("Optional parameters")
        if optional_names:
            optional_values = _render_text_grid(optional_names, key_prefix=f"{key_prefix}:optional")
        else:
            st.caption("선택 쿼리 파라미터가 없습니다.")
            optional_values = {}

        kind, page_no, num_of_rows = _render_common_options(key_prefix)

        st.subheader("Conditions (cond[FIELD::OP])")
        st.caption(
            "이력조회(history)는 보통 BASE_DATE 조건이 필요합니다. "
            "증분조회는 DAT_UPDT_PNT/LAST_MDFCN_PNT를 GTE로 사용합니다."
        )
        conditions = _render_condition_rows(key_prefix)

        extra_text = st.text_area(
            "Extra params JSON",
            value="{}",
            height=90,
            help="폼에 없는 쿼리 파라미터를 JSON object로 추가합니다.",
            key=f"{key_prefix}:extra",
        )
        submitted = st.form_submit_button("Run selected API")

    params = {**required_values, **optional_values, **_parse_extra_params(extra_text)}
    missing = [name for name in required_names if not str(params.get(name, "")).strip()]
    return (
        submitted,
        {key: value for key, value in params.items() if str(value).strip()},
        {
            "kind": kind,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "conditions": conditions,
        },
        missing,
    )


def _render_text_grid(names: tuple[str, ...], *, key_prefix: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for index in range(0, len(names), 2):
        columns = st.columns(2)
        for column, name in zip(columns, names[index : index + 2], strict=False):
            with column:
                values[name] = st.text_input(name, value="", key=f"{key_prefix}:{name}")
    return values


def _render_common_options(key_prefix: str) -> tuple[str, int, int]:
    col1, col2, col3 = st.columns(3)
    with col1:
        kind = st.selectbox(
            "kind",
            list(OpenApiKind),
            format_func=_kind_label,
            key=f"{key_prefix}:kind",
        )
    with col2:
        page_no = st.number_input(
            "pageNo", min_value=1, value=1, step=1, key=f"{key_prefix}:pageNo"
        )
    with col3:
        num_of_rows = st.number_input(
            "numOfRows",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="공공데이터포털 규격상 1~100입니다.",
            key=f"{key_prefix}:numOfRows",
        )
    return str(kind.value), int(page_no), int(num_of_rows)


def _kind_label(value: OpenApiKind) -> str:
    return f"{value.value} (조회)" if value == OpenApiKind.INFO else f"{value.value} (이력조회)"


def _render_condition_rows(key_prefix: str) -> dict[str, tuple[str, str]]:
    conditions: dict[str, tuple[str, str]] = {}
    for index in range(CONDITION_ROW_COUNT):
        col1, col2, col3 = st.columns([2, 1, 2])
        show_labels = index == 0
        with col1:
            field = st.text_input(
                "Field",
                value="",
                placeholder="예: BASE_DATE, DAT_UPDT_PNT, OPN_ATMY_GRP_CD",
                key=f"{key_prefix}:cond:{index}:field",
                label_visibility="visible" if show_labels else "collapsed",
            )
        with col2:
            operator = st.selectbox(
                "Operator",
                list(ConditionOperator),
                key=f"{key_prefix}:cond:{index}:operator",
                label_visibility="visible" if show_labels else "collapsed",
            )
        with col3:
            value = st.text_input(
                "Value",
                value="",
                placeholder="예: 20260101, 3610000",
                key=f"{key_prefix}:cond:{index}:value",
                label_visibility="visible" if show_labels else "collapsed",
            )
        if field.strip():
            conditions[field.strip()] = (str(operator.value), value)
    return conditions


def _parse_extra_params(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Extra params JSON이 올바르지 않습니다: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Extra params JSON은 object여야 합니다")
    return {
        key: value
        for key, value in payload.items()
        if key not in {"serviceKey", "ServiceKey", "pageNo", "numOfRows"}
    }


def _execute_debug_request(
    selected: dict[str, Any],
    service_key: str,
    *,
    timeout: float,
    params: dict[str, Any],
    conditions: dict[str, tuple[str, str]],
    kind: str,
    page_no: int,
    num_of_rows: int,
) -> DebugRun:
    """MoisClient 생성부터 `debug_request()` 호출까지를 구조화 에러와 함께 실행합니다."""

    input_data: dict[str, Any] = {
        "slug": selected["service_key"],
        "kind": kind,
        "page_no": page_no,
        "num_of_rows": num_of_rows,
        "params": params,
        "conditions": conditions,
    }
    trace: list[str] = [f"선택한 API: {selected['dataset_label']}"]
    start = time.perf_counter()

    try:
        client = MoisClient(service_key or None, timeout=timeout, retries=0)
    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
        trace.append(f"MoisClient 생성 실패 (소요시간 {elapsed_ms}ms)")
        return DebugRun(
            function="openapi_request",
            input=redact_sensitive(jsonable(input_data)),
            request={},
            response={},
            parsed=None,
            processed=None,
            trace=tuple(trace),
            error=redact_sensitive(jsonable(error_to_dict(exc))),
        )

    trace.append("MoisClient를 생성했습니다.")
    try:
        run = client.debug_request(
            selected["service_key"],
            kind=kind,
            page_no=page_no,
            num_of_rows=num_of_rows,
            conditions=conditions,
            params=params,
        )
    finally:
        client.close()

    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
    combined_trace = (*trace, *run.trace, f"총 소요시간: {elapsed_ms}ms")
    return DebugRun(
        function=run.function,
        input=run.input,
        request=run.request,
        response=run.response,
        parsed=run.parsed,
        processed=run.processed,
        trace=combined_trace,
        error=run.error,
    )


def _pydantic_model_tab(selected: dict[str, Any]) -> None:
    run = _current_run(selected)
    if run is None:
        st.info(
            "Raw Response 탭에서 선택한 API를 실행하면 여기에서 "
            "파싱 결과(MoisResponse)를 확인합니다."
        )
        return
    if run.error:
        st.warning("실행 중 오류가 있습니다. Validation Errors 탭을 확인하세요.")
    st.json(jsonable(run.parsed))


def _processed_result_tab(selected: dict[str, Any]) -> None:
    run = _current_run(selected)
    if run is None:
        st.info("Raw Response 탭에서 API를 실행하면 가공된 item 목록을 표시합니다.")
        return
    data = jsonable(run.processed)
    if isinstance(data, list) and data:
        st.dataframe(pd.json_normalize(data, sep="."), width="stretch", hide_index=True)
    else:
        st.json(data)


def _validation_errors_tab(selected: dict[str, Any]) -> None:
    run = _current_run(selected)
    if run is None:
        st.info("아직 실행된 API가 없습니다.")
        return
    if not run.error:
        st.success("검증 오류가 없습니다(no errors).")
        return
    st.error(run.error.get("message", "실행 중 오류가 발생했습니다."))
    st.json(run.error)


def _debug_trace_tab(selected: dict[str, Any], env_names: tuple[str, ...]) -> None:
    run = _current_run(selected)

    st.subheader("Selected API")
    st.json(selected)
    st.caption(f"credential env: {', '.join(env_names)}")

    if run is None:
        st.info("아직 실행된 API가 없습니다.")
        return

    st.subheader("Request (민감정보 마스킹됨)")
    st.json(jsonable(run.request))
    st.subheader("Response status")
    st.json({"status_code": dict(run.response or {}).get("status_code")})
    st.subheader("Trace")
    for line in run.trace:
        st.write(f"- {line}")


def _fixture_tab(fixture_base_dir: str, selected: dict[str, Any]) -> None:
    run = _current_run(selected)
    if run is None:
        st.info("Raw Response 탭에서 API를 실행한 뒤 fixture를 저장할 수 있습니다.")
        st.caption("Fixture base dir")
        st.code(fixture_base_dir, language=None)
        return

    with st.expander("Save as fixture", expanded=True):
        case_name = st.text_input("Case name", value=f"{selected['service_key']}_normal")
        description = st.text_area("Description", value=f"{selected['dataset_name']} 정상 케이스")
        assertion_mode = st.selectbox(
            "Assertion mode",
            ["snapshot", "schema_only", "required_fields", "count"],
        )
        exclude_fields_raw = st.text_input(
            "Exclude fields",
            value="fetched_at, request_id, updated_at",
        )
        required_fields_raw = st.text_input("Required fields", value="")
        overwrite = st.checkbox("Overwrite existing fixture", value=False)

        assertion = {
            "mode": assertion_mode,
            "exclude_fields": [
                value.strip() for value in exclude_fields_raw.split(",") if value.strip()
            ],
            "required_fields": [
                value.strip() for value in required_fields_raw.split(",") if value.strip()
            ],
        }

        st.subheader("Fixture preview")
        st.json(
            {
                "function": run.function,
                "input": jsonable(run.input),
                "request": jsonable(run.request),
                "response": jsonable(run.response),
                "processed": jsonable(run.processed),
                "assertion": assertion,
            }
        )

        if st.button("Save as fixture"):
            try:
                path = save_fixture(
                    base_dir=fixture_base_dir,
                    function_name=run.function,
                    case_name=case_name,
                    description=description,
                    input_data=run.input,
                    request_data=run.request,
                    response_data=run.response,
                    parsed_result=run.parsed,
                    processed_result=run.processed,
                    assertion=assertion,
                    overwrite=overwrite,
                )
            except Exception as exc:
                st.error(f"{exc.__class__.__name__}: {exc}")
                st.json(redact_sensitive(jsonable(error_to_dict(exc))))
            else:
                st.success(f"Saved: {path}")


def _api_summary_line(selected: dict[str, Any]) -> str:
    name = selected["dataset_name"]
    return f"{name} 업종의 인허가 현황을 조회하는 지방행정 인허가정보 OpenAPI입니다."


def _api_response_line(selected: dict[str, Any]) -> str:
    return f"조회: {selected['info_operation']} / 이력조회: {selected['history_operation']}"


def _env_key_value(env_names: tuple[str, ...]) -> str | None:
    for name in env_names:
        value = os.getenv(name)
        if value is not None and value.strip():
            return value
    return None


def _fixture_base_dir_sidebar() -> str:
    st.sidebar.subheader("Fixtures")
    candidates = _fixture_dir_candidates()
    options = [str(path) for path in candidates]
    custom_label = "Custom..."
    selected = st.sidebar.selectbox("Fixture base dir", [*options, custom_label])
    if selected == custom_label:
        selected = st.sidebar.text_input(
            "Custom fixture base dir",
            value=str(DEFAULT_FIXTURE_DIR),
        )
    st.sidebar.caption(selected)
    return selected


def _fixture_dir_candidates() -> list[Path]:
    preferred = [DEFAULT_FIXTURE_DIR, ROOT / "tests", ROOT / "examples", ROOT]
    candidates: list[Path] = []
    for path in preferred:
        resolved = path.resolve()
        if resolved not in candidates:
            candidates.append(resolved)
    return candidates


def _store_run(selected: dict[str, Any], kind: str, run: DebugRun) -> None:
    st.session_state["last_run"] = {"selection_key": _selection_key(selected, kind), "run": run}


def _current_run(selected: dict[str, Any]) -> DebugRun | None:
    stored = st.session_state.get("last_run")
    if not isinstance(stored, dict):
        return None
    key = str(stored.get("selection_key", ""))
    if not key.startswith(f"{selected['data_source']}:{selected['service_key']}:"):
        return None
    run = stored.get("run")
    return run if isinstance(run, DebugRun) else None


def _selection_key(selected: dict[str, Any], kind: str) -> str:
    return f"{selected['data_source']}:{selected['service_key']}:{kind}"


if __name__ == "__main__":
    main()
