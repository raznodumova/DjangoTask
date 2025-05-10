"""
Основная URL-конфигурация проекта DjangoApi.

Содержит только:
- Маршрут к админ-панели Django
- Подключение всех URL-ов приложения app
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
