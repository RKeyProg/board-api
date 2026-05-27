from fastapi import FastAPI
from app.projects import routes as projects_routes

app = FastAPI()

app.include_router(projects_routes.router)
