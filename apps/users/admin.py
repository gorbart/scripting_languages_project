from django.contrib import admin

from apps.users.models import AppUser

admin.site.register(AppUser)
