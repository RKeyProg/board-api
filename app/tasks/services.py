import logging
from typing import Annotated

from fastapi import Depends
from app.tasks.repository import TaskRepository, TaskRepositoryDep

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get(self, task_id: int):
        try:
            return self.repo.get_by_id(task_id)
        except ValueError as e:
            logger.error("Error: %s", e, exc_info=True)


def get_task_service(repo: TaskRepositoryDep):
    return TaskService(repo)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
