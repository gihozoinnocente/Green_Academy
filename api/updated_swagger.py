"""
Updated Swagger documentation with all API endpoints according to API_DESIGN.md.
"""

from .swagger_auth import AUTH_PATHS, AUTH_COMPONENTS
from .swagger_users import USER_PATHS, USER_COMPONENTS
from .swagger_courses import COURSE_PATHS
from .swagger_enrollments import ENROLLMENT_PATHS

# Generate the complete OpenAPI spec
def get_swagger_spec() -> dict:
    """Get the complete Swagger specification."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Green Academy API",
            "version": "1.0.0",
            "description": "API for Green Academy educational platform",
            "contact": {
                "email": "contact@greenacademy.com"
            },
            "license": {
                "name": "BSD License"
            }
        },
        "servers": [
            {
                "url": "/api",
                "description": "Green Academy API"
            }
        ],
        "paths": {
            # Authentication endpoints
            "/auth/login/": AUTH_PATHS["/auth/login/"],
            "/auth/refresh/": AUTH_PATHS["/auth/refresh/"],
            "/auth/verify/": AUTH_PATHS["/auth/verify/"],
            
            # User endpoints
            "/users/": USER_PATHS["/users/"],
            "/users/{id}/": USER_PATHS["/users/{id}/"],
            "/users/me/": USER_PATHS["/users/me/"],

            # Course endpoints
            "/courses/": COURSE_PATHS["/courses/"],
            "/courses/{id}/": COURSE_PATHS["/courses/{id}/"],

            # Enrollment endpoints
            "/enrollments/": ENROLLMENT_PATHS["/enrollments/"],
            "/enrollments/{id}/": ENROLLMENT_PATHS["/enrollments/{id}/"],
        },
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            },
            "schemas": {
                # Authentication schemas
                "LoginRequest": AUTH_COMPONENTS["LoginRequest"],
                "TokenResponse": AUTH_COMPONENTS["TokenResponse"],
                "RefreshRequest": AUTH_COMPONENTS["RefreshRequest"],
                "VerifyRequest": AUTH_COMPONENTS["VerifyRequest"],
                
                # User schemas
                "User": USER_COMPONENTS["User"],
                "UserCreate": USER_COMPONENTS["UserCreate"],
                "UserUpdate": USER_COMPONENTS["UserUpdate"],
                "UserPartialUpdate": USER_COMPONENTS["UserPartialUpdate"],
            }
        }
    }
