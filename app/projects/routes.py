from fastapi import APIRouter, Depends, HTTPException

from app.projects.schema import (
    ProjectCreateRequest,
    ProjectCreateResponse,
    ProjectGetResponse,
    ProjectPath,
    ProjectUpdateRequest,
    ProjectUpdateResponse,
)
from app.projects.service import ProjectServiceDep

router = APIRouter(prefix="/v1/projects", tags=["Projects"])


@router.get("/{project_id}")
async def get_project(service: ProjectServiceDep, path: ProjectPath = Depends()):
    project = await service.get(path.project_id)
    if project is None:
        raise HTTPException(404, detail="Project not found")
    return ProjectGetResponse(
        id=project.id,
        key=project.key,
        name=project.name,
        description=project.description,
    )


@router.post("/")
async def create_project(service: ProjectServiceDep, data: ProjectCreateRequest):
    res = await service.create(data)
    return ProjectCreateResponse(id=res.id, name=res.name)


@router.patch("/{project_id}")
async def update_project(
    service: ProjectServiceDep,
    data: ProjectUpdateRequest,
    path: ProjectPath = Depends(),
):
    project = await service.update(path.project_id, data)
    if project is None:
        raise HTTPException(404, detail="Project not found")
    return ProjectUpdateResponse(
        id=project.id,
        key=project.key,
        name=project.name,
        description=project.description,
    )


@router.delete("/{project_id}")
async def delete_project(service: ProjectServiceDep, path: ProjectPath = Depends()):
    success = await service.delete(path.project_id)
    if not success:
        raise HTTPException(404, detail="Project not found")
    return {"message": "Project deleted successfully"}
