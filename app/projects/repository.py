import logging
from typing import Annotated

from fastapi import Depends
from app.core.db import DbSessionDep
from app.projects.model import Project

logger = logging.getLogger(__name__)


class ProjectRepository:
    def __init__(self, db_session: DbSessionDep):
        self.db_session = db_session

    async def get_by_id(self, project_id: int):
        return await self.db_session.get(Project, project_id)

    async def save(self, project: Project):
        self.db_session.add(project)
        await self.db_session.commit()
        await self.db_session.refresh(project)
        return project

    async def delete(self, project: Project):
        await self.db_session.delete(project)
        await self.db_session.commit()
        return True


async def get_project_repository(db_session: DbSessionDep):
    return ProjectRepository(db_session)


ProjectRepositoryDep = Annotated[ProjectRepository, Depends(get_project_repository)]
