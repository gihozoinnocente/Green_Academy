# Create a new file: api/middleware.py

import logging
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger('auth')

class AuthLoggingMiddleware(MiddlewareMixin):
    """Middleware to log authentication attempts and failures"""
    
    def process_request(self, request):
        # Skip logging for certain paths
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
            
        # Log token requests
        if request.path == '/api/user/login/' and request.method == 'POST':
            try:
                body = json.loads(request.body)
                email = body.get('email', '')
                if email:
                    logger.info(f"Login attempt for user: {email}")
            except:
                pass
                
        return None
    
    def process_response(self, request, response):
        # Log authentication failures
        if (request.path == '/api/user/login/' and 
            request.method == 'POST' and 
            response.status_code != 200):
            try:
                body = json.loads(request.body)
                email = body.get('email', '')
                if email:
                    logger.warning(f"Failed login attempt for user: {email}")
            except:
                pass
                
        return response
        

class RoleCheckMiddleware(MiddlewareMixin):
    """Middleware to validate user role access to specific URL patterns"""
    
    def process_request(self, request):
        # Skip for authentication endpoints and static files
        if (request.path.startswith('/api/user/login/') or 
            request.path.startswith('/api/user/token/refresh/') or
            request.path.startswith('/static/') or
            request.path.startswith('/admin/')):
            return None
            
        # Skip if not authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return None
            
        # Role-based path checking
        user = request.user
        
        # Admin can access everything
        if user.role == 'admin':
            return None
            
        # Check teacher endpoints
        if request.path.startswith('/api/teacher/') and user.role != 'teacher' and user.role != 'admin':
            return JsonResponse({
                "detail": "You do not have permission to access this resource."
            }, status=403)
            
        # Check student endpoints
        if request.path.startswith('/api/student/') and user.role != 'student' and user.role != 'admin':
            return JsonResponse({
                "detail": "You do not have permission to access this resource."
            }, status=403)
            
        return None