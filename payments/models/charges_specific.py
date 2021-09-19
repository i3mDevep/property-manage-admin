from django.db import models
from coproperties.models import Property

from utils.models import ModelCustom


class ChargesSpecific(ModelCustom):

    TYPE_STATUS_CHOICES = (
        ("FINALIZED", "Finalized"),
        ("OPEN", "Open"),
        ("SUSPEND", "Suspend"),
    )

    status = models.CharField(max_length=15,
                              choices=TYPE_STATUS_CHOICES,
                              default="OPEN")

    reason = models.CharField(max_length=100)

    description = models.TextField(null=True, blank=True)

    property = models.ForeignKey(
        Property, related_name="charges_specific", on_delete=models.CASCADE)

    money = models.DecimalField(max_digits=15, decimal_places=2)
