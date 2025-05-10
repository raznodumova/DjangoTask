"""
Модуль API endpoints для управления задачами и пользователями.

Содержит ViewSets для работы с основными сущностями системы:
- TaskSet: управление задачами с JWT-аутентификацией
- UserSet: управление пользователями (администраторский функционал)
"""

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TaskSerializer, UserSerializer
from .models import Task


class TaskSet(ModelViewSet):
    """ ViewSet для операций CRUD с задачами.

    Особенности:
    - Использует JWT-аутентификацию
    - Требует аутентификации для доступа
    - Фильтрует задачи по текущему пользователю
    - Автоматически назначает владельца при создании

    Поддерживаемые методы:
    GET /api/tasks/ - список задач пользователя
    POST /api/tasks/ - создание новой задачи
    GET/PUT/PATCH/DELETE /api/tasks/{id}/ - работа с конкретной задачей

    Поля задачи:
    - title (строка): название задачи
    - description (текст): описание задачи
    - status (выбор): new/in_progress/completed
    - owner (readonly): владелец задачи """
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.none()

    def get_queryset(self):
        """Возвращает кверисет задач, отфильтрованный по текущему пользователю.

        Переопределяет базовую реализацию для обеспечения безопасности данных.
        Пользователь видит только свои задачи."""
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Создает задачу с автоматическим назначением владельца.

        Параметры:
        - serializer: экземпляр TaskSerializer с валидированными данными

        Автоматически добавляет текущего пользователя в поле owner перед сохранением."""
        serializer.save(owner=self.request.user)


class UserSet(ModelViewSet):
    """ Администраторский ViewSet для управления пользователями.

    Особенности:
    - Доступен только пользователям с правами администратора
    - Использует JWT-аутентификацию
    - Пароли хранятся в хешированном виде
    - Поле password доступно только для записи

    Поддерживаемые методы:
    GET /api/users/ - список всех пользователей
    POST /api/users/ - создание нового пользователя
    GET/PUT/PATCH/DELETE /api/users/{id}/ - работа с конкретным пользователем

    Поля пользователя:
    - username (строка): уникальный логин
    - email (email): электронная почта
    - password (строка): пароль (только для записи) """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Ограничение на удаление пользователей.
        Даже админы не могут удалять пользователей через API.
        """
        if self.action == 'destroy':
            return [IsAdminUser() & IsAuthenticated()]
        return super().get_permissions()
