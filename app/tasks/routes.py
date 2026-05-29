import logging
from fastapi import APIRouter, Depends, HTTPException

from app.tasks.services import TaskServiceDep
from app.tasks.schema import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskGetResponse,
    TaskPath,
    TaskSearchParams,
    TaskSearchResponse,
)

router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])

logger = logging.getLogger(__name__)


@router.get("/{task_id}")
async def get_task(service: TaskServiceDep, path: TaskPath = Depends()):
    task = await service.get(path.task_id)
    if task is None:
        raise HTTPException(404, detail="Task not found")
    return TaskGetResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        is_completed=task.is_completed,
    )


@router.post("/")
async def create_task(service: TaskServiceDep, data: TaskCreateRequest):
    task = await service.create(data)
    if task is None:
        raise HTTPException(400, detail="Project not found")

    return TaskCreateResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        project_id=task.project_id,
    )


@router.get("/")
async def search_tasks(service: TaskServiceDep, params: TaskSearchParams = Depends()):
    tasks, total = await service.search(params)
    return TaskSearchResponse(
        items=[
            TaskGetResponse(
                id=t.id,
                title=t.title,
                description=t.description,
                project_id=t.project_id,
                is_completed=t.is_completed,
            )
            for t in tasks
        ],
        total=total,
        limit=params.limit,
        offset=params.offset,
    )
