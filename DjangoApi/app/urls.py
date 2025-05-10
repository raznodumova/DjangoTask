"""
URL-конфигурация приложения app.

Включает:
- API эндпоинты для задач и пользователей
- JWT аутентификацию
- Документацию Swagger/Redoc
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from DjangoApi.yasg import schema_view
from .api import TaskSet, UserSet


"""
Регистрация роутеров для задач и пользователей.
"""
router = DefaultRouter()
router.register(r'tasks', TaskSet, basename='task')
router.register(r'users', UserSet, basename='user')


"""
URL-конфигурация приложения app.
"""
urlpatterns = [
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
