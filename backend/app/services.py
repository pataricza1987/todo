from __future__ import annotations

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .models import Todo
from .schemas import TodoCreate, TodoUpdate


class TodoService:

    def __init__(self, db: Session):
        self.db = db

    def list_todos(self, only_open: bool | None = None) -> list[Todo]:
        stmt = select(Todo).order_by(Todo.created_at.desc())
        todos = list(self.db.execute(stmt).scalars().all())

        if only_open is None:
            return todos
        elif only_open:
            return [t for t in todos if not t.done]
        else:
            return [t for t in todos if t.done]

    def get_todo(self, todo_id: int) -> Todo | None:
        return self.db.execute(select(Todo).where(Todo.id == todo_id)).scalars().first()

    def create_todo(self, data: TodoCreate) -> Todo:
        todo = Todo(
            title=data.title,
            description=data.description,
            done=data.done,
            priority=data.priority,
            due_date=data.due_date,
        )
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update_todo(self, todo: Todo, data: TodoUpdate) -> Todo:
        if data.title is not None:
            todo.title = data.title
        if data.description is not None:
            todo.description = data.description
        if data.done is not None:
            todo.done = data.done
        if data.priority is not None:
            todo.priority = data.priority
        if data.due_date is not None:
            todo.due_date = data.due_date

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete_todo(self, todo: Todo) -> None:
        self.db.delete(todo)
        self.db.commit()

    def enrich_with_quote(self, todo: Todo) -> Todo:
        todo.last_quote = self._fetch_quote_text()
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def _fetch_quote_text(self) -> str:
        try:
            r = requests.get(settings.quote_api_url, timeout=5)
            r.raise_for_status()
            data = r.json()
            content = data.get("value") or ""
            if content:
                return content[:500]
        except Exception:
            pass
        return "Fallback idézet: csináld meg ma, hogy holnap nyugi legyen."
