"""
Сериализаторы для моделей задач и пользователей.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с обработкой пароля."""
    class Meta:
        """Конфигурация сериализатора."""
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Создание пользователя с хешированным паролем."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для модельки задач с автоматическим назначением владельца."""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Конфигурация сериализатора."""
        model = Task
        fields = ('id', 'title', 'description', 'status', 'owner')
        read_only_fields = ('owner',)

    def create(self, validated_data):
        """Создание задачи и назначение текущего пользователя ее владельцем."""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
