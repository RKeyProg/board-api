from typing import Annotated

from fastapi import Depends


class TaskRepository:
    def get_by_id(self, task_id: int):
        return task_id


def get_task_repository():
    return TaskRepository()


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
