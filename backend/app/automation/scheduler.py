from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from ..config import settings
from ..db import SessionLocal
from ..services import TodoService

logger = logging.getLogger(__name__)


async def run_scheduler_forever() -> None:
    interval = max(int(settings.scheduler_interval_seconds), 5)
    logger.info("Scheduler started (interval=%ss)", interval)

    while True:
        try:
            _tick_once()
        except Exception:
            logger.exception("Scheduler tick failed")

        await asyncio.sleep(interval)


def _tick_once() -> None:
    with SessionLocal() as db:
        svc = TodoService(db)
        todos = svc.list_todos(only_open=True)

        now = datetime.utcnow()
        soon = now + timedelta(hours=24)

        due_soon = [t for t in todos if t.due_date and now <= t.due_date <= soon]
        if not due_soon:
            logger.debug("scheduler: no due-soon todos")
            return

        for t in due_soon:
            before = t.last_quote
            svc.enrich_with_quote(t)
            logger.info(
                "scheduler: todo id=%s due=%s quote_updated=%s",
                t.id,
                t.due_date,
                before != t.last_quote,
            )
