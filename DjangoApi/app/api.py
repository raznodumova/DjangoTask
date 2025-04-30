"""
API для DjangoApi.
"""

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TaskSerializer, UserSerializer
from .models import Task


class TaskSet(ModelViewSet):
    """ API для задач. """
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.none()

    def get_queryset(self):
        """Возвращает задачи только их владельцам."""
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Сохраняет задачу владельца."""
        serializer.save(owner=self.request.user)


class UserSet(ModelViewSet):
    """ API для пользователей. """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
