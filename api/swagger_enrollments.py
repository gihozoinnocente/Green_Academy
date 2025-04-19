"""
Enrollment endpoints documentation for Swagger.
This module provides the OpenAPI spec for enrollment-related endpoints.
"""

# Enrollment endpoints documentation
ENROLLMENT_PATHS = {
    "/enrollments/": {
        "get": {
            "tags": ["Enrollments"],
            "summary": "List enrollments",
            "description": "Get a list of enrollments. Admins can see all enrollments, regular users can only see their own.",
            "operationId": "listEnrollments",
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
                    "description": "Search query string (searches user, course, status)",
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
                                        "items": {"$ref": "#/components/schemas/Enrollment"}
                                    }
                                }
                            }
                        }
                    }
                },
                "401": {"description": "Authentication required"}
            }
        },
        "post": {
            "tags": ["Enrollments"],
            "summary": "Create enrollment",
            "description": "Enroll in a course. Regular users can only enroll themselves, admins can enroll any user.",
            "operationId": "createEnrollment",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/EnrollmentCreate"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Enrollment created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Enrollment"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input or already enrolled"},
                "401": {"description": "Authentication required"},
                "404": {"description": "Course or user not found"}
            }
        }
    },
    "/enrollments/{id}/": {
        "get": {
            "tags": ["Enrollments"],
            "summary": "Get enrollment details",
            "description": "Get details of a specific enrollment. Users can only access their own enrollments, admins can access any.",
            "operationId": "getEnrollment",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the enrollment to retrieve",
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
                            "schema": {"$ref": "#/components/schemas/EnrollmentDetail"}
                        }
                    }
                },
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not the enrolled user or admin"},
                "404": {"description": "Enrollment not found"}
            }
        },
        "put": {
            "tags": ["Enrollments"],
            "summary": "Update enrollment",
            "description": "Update an enrollment's status or completion. Users can only update their own enrollments, admins can update any.",
            "operationId": "updateEnrollment",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the enrollment to update",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/EnrollmentUpdate"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Enrollment updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Enrollment"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not the enrolled user or admin"},
                "404": {"description": "Enrollment not found"}
            }
        },
        "patch": {
            "tags": ["Enrollments"],
            "summary": "Partially update enrollment",
            "description": "Partially update an enrollment's status or completion. Users can only update their own enrollments, admins can update any.",
            "operationId": "partialUpdateEnrollment",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the enrollment to partially update",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/EnrollmentUpdate"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Enrollment updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Enrollment"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not the enrolled user or admin"},
                "404": {"description": "Enrollment not found"}
            }
        },
        "delete": {
            "tags": ["Enrollments"],
            "summary": "Delete enrollment",
            "description": "Unenroll from a course. Users can only delete their own enrollments, admins can delete any.",
            "operationId": "deleteEnrollment",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the enrollment to delete",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "responses": {
                "204": {"description": "Enrollment deleted successfully"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not the enrolled user or admin"},
                "404": {"description": "Enrollment not found"}
            }
        }
    },
    "/users/{id}/enrollments/": {
        "get": {
            "tags": ["Enrollments"],
            "summary": "List user enrollments",
            "description": "Get a list of enrollments for a specific user. Users can only access their own enrollments, admins can access any.",
            "operationId": "listUserEnrollments",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the user whose enrollments to retrieve",
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
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        }
                    }
                },
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not the user or admin"},
                "404": {"description": "User not found"}
            }
        }
    },
    "/courses/{id}/enrollments/": {
        "get": {
            "tags": ["Enrollments"],
            "summary": "List course enrollments",
            "description": "Get a list of enrollments for a specific course. Admin only.",
            "operationId": "listCourseEnrollments",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the course whose enrollments to retrieve",
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
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/Enrollment"}
                            }
                        }
                    }
                },
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not admin"},
                "404": {"description": "Course not found"}
            }
        }
    }
}

# Enrollment-related schemas for Swagger documentation
ENROLLMENT_COMPONENTS = {
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
                        "type": "integer",
                        "example": 5
                    },
                    "username": {
                        "type": "string",
                        "example": "johnsmith"
                    },
                    "email": {
                        "type": "string",
                        "example": "john.smith@example.com"
                    }
                }
            },
            "course": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 3
                    },
                    "title": {
                        "type": "string",
                        "example": "Introduction to Renewable Energy"
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
                "enum": ["ACT", "COM", "PAU", "DRO"],
                "example": "ACT",
                "description": "ACT: Active, COM: Completed, PAU: Paused, DRO: Dropped"
            },
            "completion_percentage": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
                "example": 25
            }
        }
    },
    "EnrollmentDetail": {
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
                        "type": "integer",
                        "example": 5
                    },
                    "username": {
                        "type": "string",
                        "example": "johnsmith"
                    }
                }
            },
            "course": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 3
                    },
                    "title": {
                        "type": "string",
                        "example": "Introduction to Renewable Energy"
                    },
                    "description": {
                        "type": "string",
                        "example": "Learn about renewable energy sources and sustainability."
                    },
                    "instructor": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "example": 2
                            },
                            "name": {
                                "type": "string",
                                "example": "Dr. Jane Smith"
                            }
                        }
                    },
                    "duration": {
                        "type": "string",
                        "example": "6 weeks"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["BEG", "INT", "ADV"],
                        "example": "BEG"
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
                "enum": ["ACT", "COM", "PAU", "DRO"],
                "example": "ACT",
                "description": "ACT: Active, COM: Completed, PAU: Paused, DRO: Dropped"
            },
            "completion_percentage": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
                "example": 25
            }
        }
    },
    "EnrollmentCreate": {
        "type": "object",
        "required": ["course_id"],
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user to enroll (only needed for admin users creating enrollments for others)",
                "example": 5
            },
            "course_id": {
                "type": "integer",
                "description": "ID of the course to enroll in",
                "example": 3
            }
        }
    },
    "EnrollmentUpdate": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["ACT", "COM", "PAU", "DRO"],
                "example": "PAU",
                "description": "ACT: Active, COM: Completed, PAU: Paused, DRO: Dropped"
            },
            "completion_percentage": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100,
                "example": 50
            }
        }
    }
}
