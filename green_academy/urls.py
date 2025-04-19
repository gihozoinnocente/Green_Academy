import os
import redis
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import RedisError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.test_views import test_view
from api.swagger_view import swagger_ui_view
from typing import List, Union, Dict, Any
from django.urls.resolvers import URLPattern, URLResolver

# Health check endpoint to monitor system components
def health_check(request):
    # Check database connection
    try:
        connections['default'].cursor()
        db_status = True
    except OperationalError:
        db_status = False
    
    # Check Redis connection
    try:
        redis_client = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/1'))
        redis_client.ping()
        redis_status = True
    except RedisError:
        redis_status = False
    
    status = db_status and redis_status
    status_code = 200 if status else 503
    
    response: Dict[str, Any] = {
        'status': 'healthy' if status else 'unhealthy',
        'components': {
            'database': 'up' if db_status else 'down',
            'redis': 'up' if redis_status else 'down',
        }
    }
    
    return JsonResponse(response, status=status_code)


urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Root redirect to Swagger UI
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),
    
    # Simple test view to verify routing
    path('test/', test_view, name='test'),
    
    # Health check endpoint for monitoring
    path('health/', health_check, name='health_check'),
    
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom Swagger documentation URL
    path('swagger/', swagger_ui_view, name='swagger-ui'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)