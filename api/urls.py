from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver

from .views import (
    UserViewSet, CourseViewSet, EnrollmentViewSet, ModuleViewSet,
    ActivityViewSet, UserEnrollmentsView, CourseEnrollmentsView, LoginView,
    TokenVerifyView
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'modules', ModuleViewSet)
router.register(r'activities', ActivityViewSet)

# The API URLs are determined automatically by the router
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', include(router.urls)),
    path('users/<int:user_id>/enrollments/', UserEnrollmentsView.as_view(), name='user-enrollments'),
    path('courses/<int:course_id>/enrollments/', CourseEnrollmentsView.as_view(), name='course-enrollments'),
    # Privacy endpoints
    path('users/me/export/', UserViewSet.as_view({'get': 'export_personal_data'}), name='user-export-personal-data'),
    path('users/me/delete/', UserViewSet.as_view({'delete': 'delete_account'}), name='user-delete-account'),
    # Authentication URLs
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]