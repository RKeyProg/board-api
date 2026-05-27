from fastapi import APIRouter, Depends

from app.tasks.services import TaskServiceDep
from app.tasks.schema import TaskGetResponse, TaskPath

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.get("/{task_id}")
def get_task(service: TaskServiceDep, path: TaskPath = Depends()):
    res = service.get(path.task_id)
    return TaskGetResponse(task_id=res)
