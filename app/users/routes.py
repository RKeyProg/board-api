from fastapi import APIRouter, HTTPException
from app.users.schema import (
    UserLoginRequest,
    UserRegisterRequest,
    JWTResponse,
)
from app.users.service import UserServiceDep

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/register")
async def register(service: UserServiceDep, user_data: UserRegisterRequest):
    token = await service.create(user_data)
    return JWTResponse(token=token)


@router.post("/login")
async def login(service: UserServiceDep, user_data: UserLoginRequest):
    token = await service.authenticate(user_data)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return JWTResponse(token=token)
