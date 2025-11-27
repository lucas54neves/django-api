from .models import Task


def create_task(*, owner, title: str, done: bool = False) -> Task:
    return Task.objects.create(owner=owner, title=title, done=done)


def update_task(*, task: Task, **data) -> Task:
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return task


def delete_task(*, task: Task):
    task.delete()
