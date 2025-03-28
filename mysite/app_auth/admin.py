from django.contrib import admin
from .models import ProfileUser


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = "pk", "fullName", "phone", "avatar"
    list_display_links = "pk", "fullName"
    ordering = "pk",
