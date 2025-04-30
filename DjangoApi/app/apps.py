"""
Конфигурация приложения.
"""

from django.apps import AppConfig


class AppConfig(AppConfig):
    """Регистрация приложения."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
