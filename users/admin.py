from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType
from .models import Profile

admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(Profile)


