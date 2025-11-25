from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('avatar', 'bio', 'location', 'website', 'follower_count', 'following_count')}),
    )
