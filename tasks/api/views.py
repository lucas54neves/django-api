from rest_framework import permissions, viewsets

from .. import selectors, services
from ..models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return selectors.list_tasks_for_user(self.request.user)

    def perform_create(self, serializer):
        # usa o service para encapsular regra
        task = services.create_task(
            owner=self.request.user,
            title=serializer.validated_data["title"],
            done=serializer.validated_data.get("done", False),
        )
        serializer.instance = task

    def perform_update(self, serializer):
        task = self.get_object()
        services.update_task(task=task, **serializer.validated_data)

    def perform_destroy(self, instance: Task):
        services.delete_task(task=instance)
