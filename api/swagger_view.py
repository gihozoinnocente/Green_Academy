from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .swagger_courses import COURSE_PATHS, COURSE_COMPONENTS
from .swagger_enrollments import ENROLLMENT_PATHS, ENROLLMENT_COMPONENTS
from .swagger_modules import MODULE_PATHS, MODULE_COMPONENTS
from .swagger_activities import ACTIVITY_PATHS, ACTIVITY_COMPONENTS
from .swagger_users import USER_PATHS, USER_COMPONENTS

from django.http import HttpRequest

@csrf_exempt
def swagger_ui_view(request: HttpRequest) -> HttpResponse:
    """A simple view to serve Swagger UI documentation."""
    
    # Define the complete Swagger specification including all endpoints
    # Build the paths dictionary step by step
    paths = {}
    paths.update(COURSE_PATHS)
    paths.update(ENROLLMENT_PATHS)
    paths.update(MODULE_PATHS)
    paths.update(ACTIVITY_PATHS)
    paths.update(USER_PATHS)
    # Add authentication endpoints
    paths["/auth/login/"] = {
        "post": {
            "tags": ["Authentication"],
            "summary": "User login",
            "description": "Authenticate using username/email and password. Returns access and refresh tokens.",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "User's username",
                                    "example": "johndoe"
                                },
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "description": "User's email (alternative to username)",
                                    "example": "john.doe@example.com"
                                },
                                "password": {
                                    "type": "string",
                                    "format": "password",
                                    "description": "User's password",
                                    "example": "secure_password123"
                                }
                            },
                            "oneOf": [
                                {"required": ["username", "password"]},
                                {"required": ["email", "password"]}
                            ]
                        }
                    }
                }
            },
            "responses": {
                "200": {"description": "Login successful"},
                "401": {"description": "Unauthorized - Invalid credentials"}
            }
        }
    }
    paths["/auth/refresh/"] = {
        "post": {
            "tags": ["Authentication"],
            "summary": "Refresh token",
            "description": "Get a new access token using a valid refresh token",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "refresh": {
                                    "type": "string",
                                    "description": "Refresh token"
                                }
                            },
                            "required": ["refresh"]
                        }
                    }
                }
            },
            "responses": {
                "200": {"description": "New access token generated"},
                "401": {"description": "Invalid or expired refresh token"}
            }
        }
    }

    swagger_spec = {
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
        "paths": paths,
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            },
            "schemas": {
                # --- User schemas below ---
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "format": "int64",
                            "readOnly": True
                        },
                        "username": {
                            "type": "string"
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "first_name": {
                            "type": "string"
                        },
                        "last_name": {
                            "type": "string"
                        },
                        "role": {
                            "type": "string",
                            "description": "User role: student, instructor, or admin. Defaults to admin if not provided.",
                            "enum": ["student", "instructor", "admin"],
                            "example": "admin",
                            "default": "admin"
                        },
                        "date_joined": {
                            "type": "string",
                            "format": "date-time",
                            "readOnly": True
                        },
                        "is_active": {
                            "type": "boolean",
                            "readOnly": True
                        },
                        "is_staff": {
                            "type": "boolean",
                            "readOnly": True
                        }
                    }
                },
                "UserCreate": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {
                            "type": "string"
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "password": {
                            "type": "string",
                            "format": "password"
                        },
                        "first_name": {
                            "type": "string"
                        },
                        "last_name": {
                            "type": "string"
                        },
                        "role": {
                            "type": "string",
                            "description": "User role: student, instructor, or admin. Defaults to admin if not provided.",
                            "enum": ["student", "instructor", "admin"],
                            "example": "admin",
                            "default": "admin"
                        }
                    }
                },
                "UserUpdate": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string"
                        },
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "password": {
                            "type": "string",
                            "format": "password"
                        },
                        "first_name": {
                            "type": "string"
                        },
                        "last_name": {
                            "type": "string"
                        },
                        "role": {
                            "type": "string",
                            "description": "User role: student, instructor, or admin. Defaults to admin if not provided.",
                            "enum": ["student", "instructor", "admin"],
                            "example": "admin",
                            "default": "admin"
                        }
                    }
                }
            }
        }
    }
    
    # Add course schemas
    for key, value in COURSE_COMPONENTS.items():
        swagger_spec["components"]["schemas"][key] = value
    
    # Add enrollment schemas
    for key, value in ENROLLMENT_COMPONENTS.items():
        swagger_spec["components"]["schemas"][key] = value
    
    # Add module, activity, and user components
    for key, value in MODULE_COMPONENTS.items():
        swagger_spec["components"]["schemas"][key] = value
    
    for key, value in ACTIVITY_COMPONENTS.items():
        swagger_spec["components"]["schemas"][key] = value
    
    for key, value in USER_COMPONENTS.items():
        swagger_spec["components"]["schemas"][key] = value
    
    # Convert the Python dictionary to JSON string
    swagger_spec_json = json.dumps(swagger_spec)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Green Academy API - Swagger UI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>

        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const spec = {swagger_spec_json};
            
            const ui = SwaggerUIBundle({{
                spec: spec,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            }});
            window.ui = ui;
        }});
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content)