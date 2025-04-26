from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Модель задачи.
    Атрибуты:
        title - название задачи;
        description - описание задачи;
        status - статус задачи;
        owner - владелец задачи."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает название задачи."""
        return self.title
