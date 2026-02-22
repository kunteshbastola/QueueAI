from django.urls import path
from .views import register_api, logout_view, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_api, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
