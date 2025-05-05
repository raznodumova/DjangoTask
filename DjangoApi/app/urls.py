"""
URLs для DjangoApi.

Схема URL-адресов:
api/ - API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import TaskSet, UserSet

router = DefaultRouter()
router.register(r'tasks', TaskSet, basename='task')
router.register(r'users', UserSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
]
