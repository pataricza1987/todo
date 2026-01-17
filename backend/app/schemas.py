from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    done: bool = False
    priority: int = Field(3, ge=1, le=5)
    due_date: datetime | None = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    done: bool | None = None
    priority: int | None = Field(None, ge=1, le=5)
    due_date: datetime | None = None


class TodoOut(TodoBase):
    id: int
    last_quote: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
