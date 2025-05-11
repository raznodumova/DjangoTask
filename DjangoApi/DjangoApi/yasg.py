"""
YASG для DjangoApi
Выгрузка документации API Swagger и Redoc.
"""

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="API for managing users and tasks",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)
