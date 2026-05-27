from typing import Annotated

from fastapi import Depends

from app.projects.db import DBSessionDep, FakeSession


class ProjectRepository:
    def __init__(self, session: FakeSession):
        self.session = session

    def get_by_id(self, project_id: int):
        return project_id


def get_project_repository(session: DBSessionDep):
    return ProjectRepository(session)


ProjectRepositoryDep = Annotated[ProjectRepository, Depends(get_project_repository)]
