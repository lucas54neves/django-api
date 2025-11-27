from .models import Task

def list_tasks_for_user(user):
    return Task.objects.filter(owner=user).order_by('-created_at')

def get_task_for_user(*, user, task_id: int):
    return Task.objects.filter(owner=user, id=task_id).first()
