"""
URLs для DjangoApi.

Схема URL-адресов:
api/ - API
api/token/ - токены
api/token/refresh/ - обновление токена

swagger/ - документация API
redoc/ - документация API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from DjangoApi.yasg import schema_view
from .api import TaskSet, UserSet

router = DefaultRouter()
router.register(r'tasks', TaskSet, basename='task')
router.register(r'users', UserSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]
