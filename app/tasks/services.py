import logging
from typing import Annotated

from fastapi import Depends
from app.tasks.model import Task
from app.tasks.repository import TaskRepository, TaskRepositoryDep
from app.tasks.schema import TaskCreateRequest, TaskSearchParams
from app.projects.repository import ProjectRepository, ProjectRepositoryDep

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    async def get(self, task_id: int):
        return await self.task_repo.get_by_id(task_id)

    async def create(self, data: TaskCreateRequest):
        project = await self.project_repo.get_by_id(data.project_id)
        if project is None:
            return None

        task = Task(
            title=data.title,
            description=data.description,
            project_id=data.project_id,
            is_completed=False,
        )

        return await self.task_repo.save(task)

    async def search(self, params: TaskSearchParams) -> tuple[list[Task], int]:
        return await self.task_repo.search(
            offset=params.offset, limit=params.limit, project_id=params.project_id
        )


def get_task_service(task_repo: TaskRepositoryDep, project_repo: ProjectRepositoryDep):
    return TaskService(task_repo, project_repo)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
