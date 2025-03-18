from fastapi import FastAPI
from app.routes.get_tasks import router as get_tasks_router
from app.routes.create_task import router as create_task_router
from app.routes.update_task import router as update_task_router
from app.routes.delete_task import router as delete_task_router

app = FastAPI()

app.include_router(get_tasks_router, prefix="/api")
app.include_router(create_task_router, prefix="/api")
app.include_router(update_task_router, prefix="/api")
app.include_router(delete_task_router, prefix="/api")