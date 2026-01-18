import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.schemas import TodoCreate, TodoOut, TodoUpdate
from backend.app.services import TodoService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/todos")


def service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(db)


@router.get("", response_model=list[TodoOut])
def list_todos(only_open: bool | None = None, svc: TodoService = Depends(service)):
    return svc.list_todos(only_open=only_open)


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(body: TodoCreate, svc: TodoService = Depends(service)):
    return svc.create_todo(body)


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, svc: TodoService = Depends(service)):
    todo = svc.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, body: TodoUpdate, svc: TodoService = Depends(service)):
    todo = svc.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return svc.update_todo(todo, body)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, svc: TodoService = Depends(service)):
    todo = svc.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    svc.delete_todo(todo)
    return None


@router.post("/{todo_id}/enrich", response_model=TodoOut)
def enrich_todo(todo_id: int, svc: TodoService = Depends(service)):
    todo = svc.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    try:
        return svc.enrich_with_quote(todo)
    except Exception as e:
        logger.exception("enrich failed")
        raise HTTPException(status_code=500, detail=str(e))

