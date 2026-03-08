from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="SQMS API",
        default_version='v1',
        description="Smart Queue Management System API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # This allows anyone to view
)

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/')),  # Redirect root to Swagger
    path('admin/', admin.site.urls),

# queue system API endpoints
    path('api/queue/', include('queue_system.urls')),

# accounts API endpoints
    path('api/accounts/', include('accounts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]