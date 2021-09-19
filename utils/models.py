from django.db import models

""" 
    This common model for diferents uses
"""

class ModelCustom(models.Model):

    created_at = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text="Date time object created"
    )

    modified_at = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text="Save method update this field"
    )

    class Meta:
        abstract = True