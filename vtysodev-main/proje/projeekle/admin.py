from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Proje, Task

admin.site.register(Proje)
admin.site.register(Task)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)
