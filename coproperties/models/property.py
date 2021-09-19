from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.models import ModelCustom

from utils.constants import ROLE_PROPERTY

from coproperties.models import Coproperty


class Property(ModelCustom):

    TYPE_PROPERTY_CHOICES = (
        ("APTO", "Apto"),
        ("PARK", "Park"),
    )

    apto = models.CharField(max_length=100)

    block = models.IntegerField("block")

    client = models.ForeignKey(
        User, related_name="property", on_delete=models.CASCADE)

    coproperty = models.ForeignKey(
        Coproperty, related_name="property", on_delete=models.SET_NULL, null=True, blank=True)

    type_property = models.CharField(max_length=9,
                                     choices=TYPE_PROPERTY_CHOICES,
                                     default="APTO")

    emails = models.EmailField(blank=True)

    clustering_coefficient = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )

    agrouping = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )

    def validate_client_role(self):
        for group in self.client.groups.all():
            if group.name == ROLE_PROPERTY:
                return False
        return True

    def save(self, *args, **kwargs):
        if self.validate_client_role():
            raise ValidationError(f'you must be role {ROLE_PROPERTY}')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.apto)
