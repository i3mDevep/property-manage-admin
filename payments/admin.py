from django.contrib import admin

# Register your models here.

from .models import ChargesGeneral, ChargesSpecific

admin.site.register(ChargesGeneral)
admin.site.register(ChargesSpecific)

