
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('library/', include('library.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/token/', CustomTokenObtainPairView.as_view(), name='login_token_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
