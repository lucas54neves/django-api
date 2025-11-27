from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class Task(TimeStampedModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
