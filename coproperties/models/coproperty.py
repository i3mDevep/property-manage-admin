from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

from utils.models import ModelCustom
from bussiness.models import Business
from utils.constants import ROLE_COPROPERTY

class Coproperty(ModelCustom):

    name = models.CharField(max_length=100)

    business = models.ForeignKey(
        Business, related_name="coproperty", on_delete=models.SET_NULL, null=True, blank=True)

    user_coproperty = models.ForeignKey(User, related_name="coproperty", on_delete=models.CASCADE)

    logo_coproperty = models.ImageField(
        'logo_coproperty',
        upload_to='images/logo/coproperty',
        blank=True,
        null=True
    )

    def validate_client_role(self):
        for group in self.user_coproperty.groups.all():
            if group.name == ROLE_COPROPERTY:
                return False
        return True

    def save(self, *args, **kwargs):
        if self.validate_client_role():
            raise ValidationError(f'you must be role {ROLE_COPROPERTY}')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

