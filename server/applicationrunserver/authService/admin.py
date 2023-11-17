from django.contrib import admin
from .models import UserServer

class UserServerAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'name', 'lastname', 'phone', 'role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']

admin.site.register(UserServer, UserServerAdmin)