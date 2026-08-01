from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router

app = FastAPI(title="Job Search Platform", version="0.1.0")
app.include_router(health_router)
