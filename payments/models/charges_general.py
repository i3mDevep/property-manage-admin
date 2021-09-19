from django.db import models
from coproperties.models import Coproperty

from utils.models import ModelCustom

class ChargesGeneral(ModelCustom):

    status = models.BooleanField()

    name = models.CharField(max_length=100)

    description = models.TextField(null=True, blank=True)
    
    coproperty = models.OneToOneField(Coproperty, related_name="charges_general", on_delete=models.CASCADE)

    money = models.DecimalField(max_digits=15, decimal_places=2)
