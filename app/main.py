from fastapi import FastAPI

from app.routes.auth.auth_register import router as register_router
from app.routes.auth.auth_login import router as login_router

from app.routes.tasks.get_tasks import router as get_tasks_router
from app.routes.tasks.create_task import router as create_task_router
from app.routes.tasks.update_task import router as update_task_router
from app.routes.tasks.delete_task import router as delete_task_router


app = FastAPI()

# Auth endpoints.
app.include_router(register_router, prefix="/api/auth")
app.include_router(login_router, prefix="/api/auth")

# Public endpoint.
app.include_router(get_tasks_router, prefix="/api")

# Protected endpoints (all will require a valid token).
app.include_router(create_task_router, prefix="/api")
app.include_router(update_task_router, prefix="/api")
app.include_router(delete_task_router, prefix="/api")