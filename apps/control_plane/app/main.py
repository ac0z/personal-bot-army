from fastapi import FastAPI
from apps.control_plane.app.api.routes.health import router as health_router
from apps.control_plane.app.api.routes.status import router as status_router
from apps.control_plane.app.api.routes.bots import router as bots_router

from apps.control_plane.app.core.logging import setup_logging

def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Personal Bot Army - Control Plane",
        version="0.1.0",
    )

    app.include_router(health_router, tags=["health"])
    app.include_router(status_router, tags=["status"])
    app.include_router(bots_router, prefix="/bots", tags=["bots"])

    return app

app = create_app()