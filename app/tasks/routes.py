from fastapi import APIRouter, Depends

from app.core.settings import SettingsDep
from app.tasks.services import TaskServiceDep
from app.tasks.schema import TaskGetResponse, TaskPath

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.get("/{task_id}")
def get_task(
    service: TaskServiceDep, settings: SettingsDep, path: TaskPath = Depends()
):
    res = service.get(path.task_id)
    print(settings.auth.secret)
    return TaskGetResponse(task_id=res)
