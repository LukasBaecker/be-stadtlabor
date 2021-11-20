from django.contrib import admin

from .models import User, Privilege

admin.site.register(User)
admin.site.register(Privilege)