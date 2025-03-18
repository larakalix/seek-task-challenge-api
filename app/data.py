from app.models import Task, TaskStatus

tasks = [
    Task(
        id="ckx1m0a6n0000l9n3f7p1a1a",
        title="Clean the Kitchen",
        description="Wipe down countertops, clean appliances, and mop the floor.",
        status=TaskStatus.Todo,
    ),
    Task(
        id="ckx1m0a6n0001l9n3f7p1a1b",
        title="Vacuum the Living Room",
        description="Vacuum carpets, rugs, and upholstered furniture in the living area.",
        status=TaskStatus.InProgress,
    ),
    Task(
        id="ckx1m0a6n0002l9n3f7p1a1c",
        title="Do the Laundry",
        description="Sort, wash, dry, fold, and organize clothes and linens.",
        status=TaskStatus.Done,
    ),
]