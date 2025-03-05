# Create a new file: api/permissions.py

from rest_framework import permissions
from userauths.models import User

class IsAdmin(permissions.BasePermission):
    """
    Permission check for admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN

class IsTeacher(permissions.BasePermission):
    """
    Permission check for teacher users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.TEACHER

class IsStudent(permissions.BasePermission):
    """
    Permission check for student users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.STUDENT

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Permission check for both teachers and admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.TEACHER or 
            request.user.role == User.ADMIN
        )

class IsStudentOrTeacherOrAdmin(permissions.BasePermission):
    """
    Permission check for students, teachers and admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.STUDENT or
            request.user.role == User.TEACHER or 
            request.user.role == User.ADMIN
        )

class IsOwnerOrTeacherOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object, teachers, or admins to access it.
    Assumes the model instance has a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == User.ADMIN:
            return True
        
        if request.user.role == User.TEACHER and hasattr(obj, 'teacher'):
            if hasattr(obj.teacher, 'user'):
                return obj.teacher.user == request.user
            return obj.teacher == request.user
            
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False