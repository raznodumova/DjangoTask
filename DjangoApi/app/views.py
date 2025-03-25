from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated


class UserCreate(generics.CreateAPIView):
    """Вьюшка для CRUD-операций с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создание пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED, headers=headers)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения информации о пользователе."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class TaskList(generics.ListCreateAPIView):
    """Представление для получения списка задач."""
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Получение списка задач."""
        user = self.request.user
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Создание задачи."""
        serializer.save(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения информации о задаче."""
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Получение задачи."""
        user = self.request.user
        return Task.objects.filter(owner=user)

    def delete(self, request, *args, **kwargs):
        """Удаление задачи."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
