from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']  # Add fields you want to search on
    list_display = ['email', 'is_active', 'is_superuser' ]  # Add fields you want to display in the list view
    list_filter = ['is_active', 'is_staff']
admin.site.register(User, UserAdmin)
