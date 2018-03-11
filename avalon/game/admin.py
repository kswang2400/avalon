from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AvalonUser, AvalonGame

class AvalonGameAdmin(admin.ModelAdmin):
    pass

admin.site.register(AvalonUser, UserAdmin)
admin.site.register(AvalonGame, AvalonGameAdmin)
