from typing import Annotated

from fastapi import Depends
from app.tasks.repository import TaskRepository, TaskRepositoryDep


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get(self, task_id: int):
        return self.repo.get_by_id(task_id)


def get_task_service(repo: TaskRepositoryDep):
    return TaskService(repo)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
