from pydantic import BaseModel, Field, field_validator


class ProjectPath(BaseModel):
    project_id: int = Field(..., gt=0)


class ProjectCreateRequest(BaseModel):
    key: str
    name: str
    description: str | None = None

    model_config = {
        "extra": "forbid",
    }

    @field_validator("key")
    @classmethod
    def key_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Key cannot be empty")
        return v


class ProjectCreateResponse(BaseModel):
    id: int
    name: str


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectUpdateResponse(BaseModel):
    id: int
    name: str | None
    description: str | None
