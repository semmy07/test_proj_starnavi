from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from apps.core.views import RegistrationViewSet, PostEndpoint

router = routers.DefaultRouter()
router.register(r'post-endpoint', PostEndpoint)

urlpatterns = [
    path('auth-jwt/', obtain_jwt_token),
    path('auth-jwt-refresh/', refresh_jwt_token),

    path(r'', include(router.urls)),
    path('registration/', RegistrationViewSet.as_view()),
]
