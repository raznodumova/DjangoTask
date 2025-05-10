"""
URL-конфигурация для DjangoApi.

Схема URL-адресов:
admin/ - админка
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('app.urls')),
]
