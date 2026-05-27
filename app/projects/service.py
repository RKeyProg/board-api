from typing import Annotated

from fastapi import Depends

from app.projects.repository import ProjectRepository, ProjectRepositoryDep


def get_project_service(repo: ProjectRepositoryDep):
    return ProjectService(repo)


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def get(self, project_id: int):
        return self.repo.get_by_id(project_id)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
