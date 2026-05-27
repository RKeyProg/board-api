from fastapi import FastAPI
from app.projects import routes as projects_routes
from app.tasks import routes as tasks_routes

app = FastAPI()

app.include_router(projects_routes.router)
app.include_router(tasks_routes.router)
