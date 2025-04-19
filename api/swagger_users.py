"""
User endpoints documentation for Swagger.
This module provides the OpenAPI spec for user-related endpoints.
"""

# User endpoints documentation
USER_PATHS = {
    "/users/": {
        "get": {
            "tags": ["Users"],
            "summary": "List all users",
            "description": "Get a paginated list of all users. Only administrators can access this endpoint.\n\n**Pagination:**\n- Use the `page` query parameter to select the page number.\n- Use the `page_size` query parameter to specify the number of results per page (default: 10, max: 100).\n- The response includes `count`, `next`, `previous`, and `results` fields to help navigate large datasets.",
            "operationId": "listUsers",
            "parameters": [
                {
                    "name": "page",
                    "in": "query",
                    "description": "Page number for pagination",
                    "required": False,
                    "schema": {"type": "integer", "minimum": 1}
                },
                {
                    "name": "page_size",
                    "in": "query",
                    "description": "Number of results per page",
                    "required": False,
                    "schema": {"type": "integer", "minimum": 1, "maximum": 100}
                },
                {
                    "name": "search",
                    "in": "query",
                    "description": "Search query string (searches username, email, first name, last name)",
                    "required": False,
                    "schema": {"type": "string"}
                }
            ],
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
                                    "next": {"type": "string", "format": "uri", "nullable": True},
                                    "previous": {"type": "string", "format": "uri", "nullable": True},
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
            "summary": "Create a new user",
            "description": "Register a new user account.",
            "operationId": "createUser",
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
                    "description": "User created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"}
            }
        }
    },
    "/users/{id}/": {
        "get": {
            "tags": ["Users"],
            "summary": "Retrieve user details",
            "description": "Get details of a specific user. Users can only retrieve their own details, while admins can retrieve any user.",
            "operationId": "getUser",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the user to retrieve",
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
            "description": "Update a specific user. Users can only update their own details, while admins can update any user.",
            "operationId": "updateUser",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the user to update",
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
                    "description": "User updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not owner or admin"},
                "404": {"description": "User not found"}
            }
        },
        "patch": {
            "tags": ["Users"],
            "summary": "Partially update user",
            "description": "Partially update a specific user. Users can only update their own details, while admins can update any user.",
            "operationId": "partialUpdateUser",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the user to partially update",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/UserPartialUpdate"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "User updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not owner or admin"},
                "404": {"description": "User not found"}
            }
        },
        "delete": {
            "tags": ["Users"],
            "summary": "Delete user",
            "description": "Delete a specific user. Users can only delete their own account, while admins can delete any user.",
            "operationId": "deleteUser",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the user to delete",
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
            "description": "Retrieve the current authenticated user's details.",
            "operationId": "getCurrentUser",
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
    "/users/me/export/": {
        "get": {
            "tags": ["Users"],
            "summary": "Export personal data",
            "description": "Export all personal data for the authenticated user as required by privacy regulations (e.g., GDPR).",
            "operationId": "exportPersonalData",
            "security": [{"Bearer": []}],
            "responses": {
                "200": {
                    "description": "Personal data exported successfully",
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
    "/users/me/delete/": {
        "delete": {
            "tags": ["Users"],
            "summary": "Delete own account",
            "description": "Delete the authenticated user's account (right to be forgotten). This action is irreversible.",
            "operationId": "deleteOwnAccount",
            "security": [{"Bearer": []}],
            "responses": {
                "204": {"description": "Account deleted successfully"},
                "401": {"description": "Authentication required"}
            }
        }
    }
}

# User-related schemas for Swagger documentation
USER_COMPONENTS = {
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
            },
            "role": {
                "type": "string",
                "description": "User role: admin, instructor, student, or unknown",
                "enum": ["admin", "instructor", "student", "unknown"],
                "readOnly": True
            }
        }
    },
    "UserCreate": {
        "type": "object",
        "required": ["username", "password"],
        "properties": {
            "username": {
                "type": "string",
                "example": "johndoe"
            },
            "email": {
                "type": "string",
                "format": "email",
                "example": "john.doe@example.com"
            },
            "password": {
                "type": "string",
                "format": "password",
                "example": "securepassword123"
            },
            "first_name": {
                "type": "string",
                "example": "John"
            },
            "last_name": {
                "type": "string",
                "example": "Doe"
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
        "required": ["username", "email", "first_name", "last_name"],
        "properties": {
            "username": {
                "type": "string",
                "example": "johndoe"
            },
            "email": {
                "type": "string",
                "format": "email",
                "example": "john.doe@example.com"
            },
            "password": {
                "type": "string",
                "format": "password",
                "example": "newsecurepassword123"
            },
            "first_name": {
                "type": "string",
                "example": "John"
            },
            "last_name": {
                "type": "string",
                "example": "Doe"
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
    "UserPartialUpdate": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "example": "johndoe"
            },
            "email": {
                "type": "string",
                "format": "email",
                "example": "john.doe@example.com"
            },
            "password": {
                "type": "string",
                "format": "password",
                "example": "newsecurepassword123"
            },
            "first_name": {
                "type": "string",
                "example": "John"
            },
            "last_name": {
                "type": "string",
                "example": "Doe"
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
