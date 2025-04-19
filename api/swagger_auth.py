"""
Authentication endpoints documentation for Swagger.
This module provides the OpenAPI spec for auth-related endpoints.
"""

# Authentication endpoints documentation
AUTH_PATHS = {
    "/auth/login/": {
        "post": {
            "tags": ["Authentication"],
            "summary": "User login",
            "description": "Authenticate using username/email and password. Returns access and refresh tokens.",
            "operationId": "login",
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
                    "description": "Login successful",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "refresh": {
                                        "type": "string",
                                        "description": "JWT refresh token"
                                    },
                                    "access": {
                                        "type": "string", 
                                        "description": "JWT access token"
                                    },
                                    "user": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "username": {"type": "string"},
                                            "email": {"type": "string"},
                                            "first_name": {"type": "string"},
                                            "last_name": {"type": "string"},
                                            "is_staff": {"type": "boolean"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "400": {
                    "description": "Bad request - Missing required fields"
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
            "summary": "Refresh access token",
            "description": "Use a valid refresh token to get a new access token.",
            "operationId": "refreshToken",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "required": ["refresh"],
                            "properties": {
                                "refresh": {
                                    "type": "string",
                                    "description": "JWT refresh token"
                                }
                            }
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Token refresh successful",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "access": {
                                        "type": "string",
                                        "description": "New JWT access token"
                                    }
                                }
                            }
                        }
                    }
                },
                "401": {
                    "description": "Unauthorized - Invalid or expired refresh token"
                }
            }
        }
    },
    "/auth/verify/": {
        "post": {
            "tags": ["Authentication"],
            "summary": "Verify access token",
            "description": "Verify that a JWT access token is valid.",
            "operationId": "verifyToken",
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "required": ["token"],
                            "properties": {
                                "token": {
                                    "type": "string",
                                    "description": "JWT access token to verify"
                                }
                            }
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Token is valid"
                },
                "401": {
                    "description": "Unauthorized - Invalid or expired token"
                }
            }
        }
    }
}

# Authentication components for Swagger schema
AUTH_COMPONENTS = {
    "LoginRequest": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "Username for login"
            },
            "email": {
                "type": "string",
                "format": "email",
                "description": "Email for login (alternative to username)"
            },
            "password": {
                "type": "string",
                "format": "password",
                "description": "Password for login"
            }
        },
        "oneOf": [
            {"required": ["username", "password"]},
            {"required": ["email", "password"]}
        ]
    },
    "TokenResponse": {
        "type": "object",
        "properties": {
            "refresh": {
                "type": "string",
                "description": "JWT refresh token"
            },
            "access": {
                "type": "string",
                "description": "JWT access token"
            }
        },
        "required": ["refresh", "access"]
    },
    "RefreshRequest": {
        "type": "object",
        "properties": {
            "refresh": {
                "type": "string",
                "description": "JWT refresh token"
            }
        },
        "required": ["refresh"]
    },
    "VerifyRequest": {
        "type": "object",
        "properties": {
            "token": {
                "type": "string",
                "description": "JWT token to verify"
            }
        },
        "required": ["token"]
    }
}
