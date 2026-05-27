from fastapi import APIRouter, Depends

from app.projects.schema import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectGetResponse,
    ProjectPath,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)
from app.projects.service import ProjectServiceDep

router = APIRouter(prefix="/v1/projects", tags=["projects"])


@router.get("/{project_id}")
def get_project(service: ProjectServiceDep, path: ProjectPath = Depends()):
    res = service.get(path.project_id)
    return ProjectGetResponse(id=res, name="test")


@router.post("/")
async def create_project(data: ProjectCreateRequest):
    print(data)
    return ProjectCreateResponse(id=1, name=data.name)


@router.patch("/{project_id}")
def update_project(data: ProjectUpdateRequest, path: ProjectPath = Depends()):
    return ProjectUpdateResponse(
        id=path.project_id, name=data.name, description=data.description
    )
