from app.features.task.commands.task_commands import TaskCommandHandler
from app.features.task.queries.task_queries import TaskQueryHandler
from app.database import db

def get_task_command_handler() -> TaskCommandHandler:
    return TaskCommandHandler(db)

def get_task_query_handler() -> TaskQueryHandler:
    return TaskQueryHandler(db)