from django.core.exceptions import ValidationError
from django.db import models

from django.contrib.auth.models import User

from utils.models import ModelCustom


class Business(ModelCustom):

    name = models.CharField(max_length=100)

    created_for = models.ForeignKey(
        User, related_name="business", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.created_for.is_staff is False:
            raise ValidationError("you must be superuser")
        super().save(*args, **kwargs)
