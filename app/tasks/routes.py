import logging
from fastapi import APIRouter, Depends, HTTPException

from app.tasks.services import TaskServiceDep
from app.tasks.schema import TaskGetResponse, TaskPath

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])

logger = logging.getLogger(__name__)


@router.get("/{task_id}")
def get_task(service: TaskServiceDep, path: TaskPath = Depends()):
    res = service.get(path.task_id)
    if not res:
        raise HTTPException(404, detail="Task not found")
    logger.info("ID: %s", res)
    return TaskGetResponse(task_id=res)
