from django.contrib import admin

# Register your models here.

from django.contrib import admin
from authapp import models


# регистрация модели пользователей в административном разделе
@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_active", "date_joined"]
    ordering = ["-date_joined"]
