from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from typing import Any, Optional


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to view/edit it.
    """
    
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # Admin users can access anything
        if request.user.is_staff:
            return True
            
        # Check if the object has a user attribute (handle User model and objects with user FK)
        if hasattr(obj, 'id') and request.user.id == obj.id:
            return True
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False
        
    def has_permission(self, request: Request, view: APIView) -> bool:
        # For user detail endpoints with user_id in URL
        user_id = view.kwargs.get('user_id')
        if user_id is not None:
            return request.user.is_staff or str(request.user.id) == str(user_id)
        return True


class IsEnrolledOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Students to view/modify their own enrollments
    - Admins to view/modify any enrollment
    """
    
    def has_permission(self, request: Request, view: APIView) -> bool:
        # Admin users can access anything
        if request.user.is_staff:
            return True
            
        # For enrollment endpoints
        enrollment_id = view.kwargs.get('pk')
        if enrollment_id is None:
            return True
            
        # For list view, the queryset is already filtered in the viewset
        if view.action == 'list':
            return True
            
        return True  # Further checked in has_object_permission
    
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # Admin users can access anything
        if request.user.is_staff:
            return True
            
        # Check if the enrollment belongs to the user
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False