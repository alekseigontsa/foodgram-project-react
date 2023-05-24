from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Создает атрибуты для работы с пользователями в панели администратора"""
    list_display = ('pk', 'username', 'first_name',
                    'last_name', 'email', 'role',)
    list_filter = ('email', 'username')
    empty_value_display = EMPTY_VALUE_DISPLAY
