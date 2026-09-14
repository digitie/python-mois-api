"""파일이 닫히기 전에 실행 중인 작업을 마치는 비동기 파일 I/O."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


async def run_file_io(fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """취소 시에도 실행 중인 파일 작업이 끝난 뒤 자원을 반환합니다."""
    task = asyncio.create_task(asyncio.to_thread(fn, *args, **kwargs))
    try:
        return await asyncio.shield(task)
    except asyncio.CancelledError:
        while not task.done():
            try:
                await asyncio.shield(task)
            except asyncio.CancelledError:
                continue
            except Exception:
                break
        if not task.cancelled():
            task.exception()
        raise
