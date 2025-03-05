"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GREEN ACADEMY APIs",
      default_version='v1',
      description="This is the API documentation for green academy project APIs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="i.gihozo@alustudent.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   #url='https://yourdomain.com',  # Replace with your actual domain
   patterns=urlpatterns,
   settings={
       'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
       'DEFAULT_INFO': 'your_project.urls.info',
       'SECURITY_DEFINITIONS': {
           'Basic': {
               'type': 'basic'
           },
       },
       'OPERATIONS_SORTER': 'alpha',
       'VALIDATOR_URL': None,
       'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'put', 'delete', 'patch'],
       'DISPLAY_OPERATION_ID': False,
       'DEFAULT_MODEL_RENDERING': 'model',
       'DEFAULT_MODEL_DEPTH': 3,
       'SWAGGER_UI_SETTINGS': {
           'schemes': ['http', 'https'],
       },
   }
)

urlpatterns = [
    path('swagger<format>/', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
    path('admin/', admin.site.urls),
    # Add something new here

    path("api/v1/", include("api.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings. STATIC_URL, document_root=settings.STATIC_ROOT)