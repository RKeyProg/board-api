from fastapi import FastAPI
from app.core.settings import Settings
from app.projects.routes import router as projects_router
from app.tasks.routes import router as tasks_router


def create_app() -> FastAPI:
    settings = Settings()

    new_app = FastAPI(
        title=settings.app.name,
        debug=settings.app.debug,
        version="0.1.0",
    )

    new_app.state.settings = settings

    new_app.include_router(projects_router)
    new_app.include_router(tasks_router)

    return new_app


app = create_app()
