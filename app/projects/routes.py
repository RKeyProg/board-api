from fastapi import APIRouter, Depends

from app.projects.schema import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectPath,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{project_id}")
def get_project(path: ProjectPath = Depends()):
    return {"id": path.project_id}


@router.post("/")
async def create_project(data: ProjectCreateRequest):
    print(data)
    return ProjectCreateResponse(id=1, name=data.name)


@router.patch("/{project_id}")
def update_project(data: ProjectUpdateRequest, path: ProjectPath = Depends()):
    return ProjectUpdateResponse(
        id=path.project_id, name=data.name, description=data.description
    )
