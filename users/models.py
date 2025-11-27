from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel

class User(AbstractUser, TimeStampedModel):
    # campos extras se quiser
    # example: job_title = models.CharField(max_length=100, blank=True)
    pass
