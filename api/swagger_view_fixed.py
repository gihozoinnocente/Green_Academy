from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .swagger_courses import COURSE_PATHS, COURSE_COMPONENTS

from django.http import HttpRequest

@csrf_exempt
def swagger_ui_view(request: HttpRequest) -> HttpResponse:
    """A simple view to serve Swagger UI documentation."""
    
    # Define the complete Swagger specification including all endpoints
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
        "paths": {
            # Authentication endpoints
            "/auth/login/": {
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
                        "200": {
                            "description": "Login successful"
                        },
                        "401": {
                            "description": "Unauthorized - Invalid credentials"
                        }
                    }
                }
            },
            "/auth/refresh/": {
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
                        "200": {
                            "description": "New access token generated"
                        },
                        "401": {
                            "description": "Invalid or expired refresh token"
                        }
                    }
                }
            },
            "/auth/verify/": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Verify token",
                    "description": "Verify that a token is valid",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "token": {
                                            "type": "string",
                                            "description": "Token to verify"
                                        }
                                    },
                                    "required": ["token"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Token is valid"
                        },
                        "401": {
                            "description": "Invalid token"
                        }
                    }
                }
            },
            
            # User endpoints
            "/users/": {
                "get": {
                    "tags": ["Users"],
                    "summary": "List users",
                    "description": "Get a list of all users (admin only)",
                    "security": [{"Bearer": []}],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "count": {"type": "integer"},
                                            "next": {"type": "string", "nullable": True},
                                            "previous": {"type": "string", "nullable": True},
                                            "results": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/User"}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "401": {"description": "Authentication required"},
                        "403": {"description": "Forbidden - not admin"}
                    }
                },
                "post": {
                    "tags": ["Users"],
                    "summary": "Create user",
                    "description": "Register a new user",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserCreate"}
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "User created successfully"
                        },
                        "400": {
                            "description": "Invalid input"
                        }
                    }
                }
            },
            "/users/{id}/": {
                "get": {
                    "tags": ["Users"],
                    "summary": "Get user",
                    "description": "Get details of a specific user",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "security": [{"Bearer": []}],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        },
                        "401": {"description": "Authentication required"},
                        "403": {"description": "Forbidden - not owner or admin"},
                        "404": {"description": "User not found"}
                    }
                },
                "put": {
                    "tags": ["Users"],
                    "summary": "Update user",
                    "description": "Update a specific user",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "security": [{"Bearer": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserUpdate"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "User updated successfully"
                        },
                        "400": {"description": "Invalid input"},
                        "401": {"description": "Authentication required"},
                        "403": {"description": "Forbidden - not owner or admin"},
                        "404": {"description": "User not found"}
                    }
                },
                "patch": {
                    "tags": ["Users"],
                    "summary": "Partially update user",
                    "description": "Partially update a specific user",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "security": [{"Bearer": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserUpdate"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "User updated successfully"
                        },
                        "400": {"description": "Invalid input"},
                        "401": {"description": "Authentication required"},
                        "403": {"description": "Forbidden - not owner or admin"},
                        "404": {"description": "User not found"}
                    }
                },
                "delete": {
                    "tags": ["Users"],
                    "summary": "Delete user",
                    "description": "Delete a specific user",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "security": [{"Bearer": []}],
                    "responses": {
                        "204": {"description": "User deleted successfully"},
                        "401": {"description": "Authentication required"},
                        "403": {"description": "Forbidden - not owner or admin"},
                        "404": {"description": "User not found"}
                    }
                }
            },
            "/users/me/": {
                "get": {
                    "tags": ["Users"],
                    "summary": "Get current user",
                    "description": "Get the current authenticated user's details",
                    "security": [{"Bearer": []}],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        },
                        "401": {"description": "Authentication required"}
                    }
                }
            },
            
            # Course endpoints
            "/courses/": COURSE_PATHS["/courses/"],
            "/courses/{id}/": COURSE_PATHS["/courses/{id}/"],
            "/courses/featured/": COURSE_PATHS["/courses/featured/"],
            
            # Enrollment endpoints (basic)
            "/enrollments/": {
                "get": {
                    "tags": ["Enrollments"],
                    "summary": "List enrollments",
                    "description": "Get a list of user enrollments",
                    "security": [{"Bearer": []}],
                    "responses": {
                        "200": {
                            "description": "Successful operation",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Enrollment"
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Authentication required"
                        }
                    }
                }
            }
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
                # User schemas
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
                        }
                    }
                },
                
                # Course schemas
                "Course": COURSE_COMPONENTS["Course"],
                "CourseDetail": COURSE_COMPONENTS["CourseDetail"],
                "CourseCreate": COURSE_COMPONENTS["CourseCreate"],
                "CoursePatch": COURSE_COMPONENTS["CoursePatch"],
                
                # Enrollment schema (basic)
                "Enrollment": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "format": "int64",
                            "readOnly": True
                        },
                        "user": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer"
                                },
                                "username": {
                                    "type": "string"
                                },
                                "email": {
                                    "type": "string"
                                }
                            }
                        },
                        "course": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer"
                                },
                                "title": {
                                    "type": "string"
                                }
                            }
                        },
                        "enrolled_at": {
                            "type": "string",
                            "format": "date-time",
                            "readOnly": True
                        },
                        "status": {
                            "type": "string",
                            "enum": ["ACT", "COM", "PAU", "DRO"]
                        },
                        "completion_percentage": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100
                        }
                    }
                }
            }
        }
    }
    
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
