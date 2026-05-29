from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app.core.db import DbSessionDep
from app.tasks.model import Task


class TaskRepository:
    def __init__(self, db_session: DbSessionDep):
        self.db_session = db_session

    async def get_by_id(self, task_id: int):
        return await self.db_session.get(Task, task_id)

    async def save(self, task: Task):
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def search(self, offset: int, limit: int, project_id: int | None = None):
        count_query = select(count()).select_from(Task)
        query = select(Task)

        if project_id is not None:
            count_query = count_query.where(Task.project_id == project_id)
            query = query.where(Task.project_id == project_id)

        total_result = await self.db_session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(Task.id).offset(offset).limit(limit)
        result = await self.db_session.execute(query)
        tasks = list(result.scalars().all())

        return tasks, total


def get_task_repository(db_session: DbSessionDep):
    return TaskRepository(db_session)


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
