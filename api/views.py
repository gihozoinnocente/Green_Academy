from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from .privacy_serializers import UserDataExportSerializer
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from typing import Any, Dict, List, Optional, Type, Union, cast

from .models import Course, Enrollment, Module, Activity
from .serializers import (
    UserSerializer, UserLimitedSerializer, CourseListSerializer,
    CourseCreateUpdateSerializer, CourseDetailSerializer,
    EnrollmentListSerializer, EnrollmentCreateSerializer,
    EnrollmentUpdateSerializer, EnrollmentDetailSerializer,
    ModuleListSerializer, ModuleCreateSerializer, ModuleDetailSerializer,
    ActivityListSerializer, ActivityCreateSerializer, ActivityDetailSerializer
)
from .permissions import IsOwnerOrAdmin, IsEnrolledOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List users with caching."""
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export_personal_data(self, request: Request) -> Response:
        """Export all personal data for the authenticated user."""
        serializer = UserDataExportSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request: Request) -> Response:
        """Allow the authenticated user to delete their own account."""
        user = request.user
        user.delete()
        return Response({'detail': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    filter_backends = [SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    """
    API endpoint for users.
    Regular users can only view and update their own profiles.
    Admin users can view and manage all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self) -> List[Any]:
        """
        Set permissions based on action:
        - create: Allow anyone to register
        - list/retrieve: Admin only for all users, but user can access their own
        - update/partial_update/destroy: Owner or admin only
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self) -> Any:
        """
        Filter queryset based on user:
        - Admin users can see all users
        - Regular users can only see themselves
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        """Get the current authenticated user's details."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List courses with caching."""
        return super().list(request, *args, **kwargs)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'instructor__username']
    """
    API endpoint for courses.
    Anyone can view courses.
    Only admin users can create, update, or delete courses.
    """
    queryset = Course.objects.all()
    
    def get_serializer_class(self) -> type[Any]:
        """Get the appropriate serializer based on the action."""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseListSerializer
    
    def get_permissions(self) -> List[Any]:
        """
        Set permissions based on action:
        - list/retrieve/featured: Allow anyone to view courses
        - create/update/partial_update/destroy: Admin only
        """
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 60))  # Cache for 1 hour
    @action(detail=False, methods=['get'])
    def featured(self, request: Request) -> Response:
        """Get featured courses."""
        featured_courses = Course.objects.filter(is_featured=True)
        page = self.paginate_queryset(featured_courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(featured_courses, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List enrollments with caching."""
        return super().list(request, *args, **kwargs)
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'course__title', 'status']
    """
    API endpoint for enrollments.
    Students can:
    - View their own enrollments
    - Create enrollments for themselves
    - Update their own enrollment status
    - Delete (unenroll from) their own enrollments
    Admins can view, create, update, and delete any enrollment.
    """
    
    def get_queryset(self) -> Any:
        """
        Filter queryset based on user:
        - Admin users can see all enrollments
        - Regular users can only see their own enrollments
        """
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        return Enrollment.objects.filter(user=user)
    
    def get_serializer_class(self) -> type[Any]:
        """Get the appropriate serializer based on the action."""
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EnrollmentUpdateSerializer
        elif self.action == 'retrieve':
            return EnrollmentDetailSerializer
        return EnrollmentListSerializer
    
    def get_permissions(self) -> List[Any]:
        """
        Set permissions based on action:
        - create: Authenticated users
        - list/retrieve/update/partial_update/destroy: Owner or admin only
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsEnrolledOrAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer: Any) -> None:
        """
        Override create to use current user if user_id is not provided.
        Only admins can create enrollments for other users.
        """
        user = self.request.user
        if not user.is_staff and serializer.validated_data.get('user') != user:
            serializer.validated_data['user'] = user
        serializer.save()
        
        # Invalidate user's enrollment cache
        cache_key = f"user_enrollments_{user.id}"
        cache.delete(cache_key)
    
    def perform_update(self, serializer: Any) -> None:
        """Invalidate cache on update."""
        enrollment = cast(Enrollment, self.get_object())
        serializer.save()
        
        # Invalidate user's enrollment cache
        cache_key = f"user_enrollments_{enrollment.user.id}"
        cache.delete(cache_key)
    
    def perform_destroy(self, instance: Any) -> None:
        """Invalidate cache on delete."""
        user_id = instance.user.id
        super().perform_destroy(instance)
        
        # Invalidate user's enrollment cache
        cache_key = f"user_enrollments_{user_id}"
        cache.delete(cache_key)


class LoginView(APIView):
    """
    API endpoint for user login.
    Allows login with either username or email along with password.
    Returns access and refresh tokens upon successful authentication.
    """
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        """
        Authenticate user and return tokens.
        
        Accepts either username or email with password for authentication.
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not password:
            return Response(
                {"error": "Password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not (username or email):
            return Response(
                {"error": "Either username or email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If email is provided but no username, try to get the user by email
        if email and not username:
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                return Response(
                    {"error": "No user found with this email address"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # Authenticate with username and password
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            # Determine user role for token response
            if user.is_staff:
                role = 'admin'
            elif user.groups.filter(name="instructors").exists():
                role = 'instructor'
            elif user.groups.filter(name="students").exists():
                role = 'student'
            else:
                role = 'student'  # fallback

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'role': role
                }
            })
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserEnrollmentsView(generics.ListAPIView):
    """API endpoint to list enrollments for a specific user."""
    serializer_class = EnrollmentListSerializer
    permission_classes = [IsOwnerOrAdmin]
    
    def get_queryset(self) -> Any:
        """Get enrollments for the specified user."""
        user_id = self.kwargs.get('user_id')
        
        # Check if we can get from cache
        cache_key = f"user_enrollments_{user_id}"
        cached_enrollments = cache.get(cache_key)
        
        if cached_enrollments is not None:
            return cached_enrollments
        
        # Get from database if not in cache
        enrollments = Enrollment.objects.filter(user_id=user_id)
        
        # Cache for 15 minutes
        cache.set(cache_key, enrollments, timeout=settings.CACHE_TTL)
        
        return enrollments


class CourseEnrollmentsView(generics.ListAPIView):
    """API endpoint to list enrollments for a specific course."""
    serializer_class = EnrollmentListSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self) -> Any:
        """Get enrollments for the specified course."""
        course_id = self.kwargs.get('course_id')
        return Enrollment.objects.filter(course_id=course_id)


class ModuleViewSet(viewsets.ModelViewSet):
    """API endpoint for modules."""
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'course__title']
    queryset = Module.objects.all()
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List modules with caching."""
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self) -> Any:
        """Filter modules by course_id if provided."""
        queryset = Module.objects.all()
        course_id = self.request.query_params.get('course_id', None)
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        return queryset
    
    def get_serializer_class(self) -> Any:
        """Get the appropriate serializer based on the action."""
        if self.action == 'list':
            return ModuleListSerializer
        elif self.action == 'retrieve':
            return ModuleDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ModuleCreateSerializer
        return ModuleListSerializer
    
    def get_permissions(self) -> List[Any]:
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            # Only instructors or admins can create/update/delete modules
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer: Any) -> None:
        """Create a new module and invalidate cache."""
        serializer.save()
        course_id = serializer.validated_data.get('course').id
        cache.delete(f"course_modules_{course_id}")
    
    def perform_update(self, serializer: Any) -> None:
        """Update a module and invalidate cache."""
        module = serializer.instance
        serializer.save()
        cache.delete(f"course_modules_{module.course.id}")
    
    def perform_destroy(self, instance: Any) -> None:
        """Delete a module and invalidate cache."""
        course_id = instance.course.id
        instance.delete()
        cache.delete(f"course_modules_{course_id}")


class ActivityViewSet(viewsets.ModelViewSet):
    """API endpoint for activities."""
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'module__title']
    queryset = Activity.objects.all()
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List activities with caching."""
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self) -> Any:
        """Filter activities by module_id if provided."""
        queryset = Activity.objects.all()
        module_id = self.request.query_params.get('module_id', None)
        if module_id is not None:
            queryset = queryset.filter(module_id=module_id)
        return queryset
    
    def get_serializer_class(self) -> Any:
        """Get the appropriate serializer based on the action."""
        if self.action == 'list':
            return ActivityListSerializer
        elif self.action == 'retrieve':
            return ActivityDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ActivityCreateSerializer
        return ActivityListSerializer
    
    def get_permissions(self) -> List[Any]:
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            # Only instructors or admins can create/update/delete activities
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer: Any) -> None:
        """Create a new activity and invalidate cache."""
        serializer.save()
        module_id = serializer.validated_data.get('module').id
        cache.delete(f"module_activities_{module_id}")
    
    def perform_update(self, serializer: Any) -> None:
        """Update an activity and invalidate cache."""
        activity = serializer.instance
        serializer.save()
        cache.delete(f"module_activities_{activity.module.id}")
    
    def perform_destroy(self, instance: Any) -> None:
        """Delete an activity and invalidate cache."""
        module_id = instance.module.id
        instance.delete()
        cache.delete(f"module_activities_{module_id}")


class TokenVerifyView(TokenViewBase):
    """API endpoint to verify that a token is valid."""
    serializer_class = TokenVerifySerializer