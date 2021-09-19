from django.contrib.auth.models import User
from django.db import models

from utils.models import ModelCustom

class Profile(ModelCustom):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user)
