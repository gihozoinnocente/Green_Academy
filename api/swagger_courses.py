"""
Course endpoints documentation for Swagger.
This module provides the OpenAPI spec for course-related endpoints.
"""

# Course endpoints documentation
COURSE_PATHS = {
    "/courses/": {
        "get": {
            "tags": ["Courses"],
            "summary": "List all courses",
            "description": "Get a list of all available courses. Anyone can access this endpoint.",
            "operationId": "listCourses",
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
                    "description": "Search query string (searches title, description, instructor)",
                    "required": False,
                    "schema": {"type": "string"}
                }
            ],
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
                                        "items": {"$ref": "#/components/schemas/Course"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["Courses"],
            "summary": "Create a new course",
            "description": "Create a new course. Only administrators can perform this action.",
            "operationId": "createCourse",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/CourseCreate"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Course created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Course"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not an admin"}
            }
        }
    },
    "/courses/{id}/": {
        "get": {
            "tags": ["Courses"],
            "summary": "Retrieve course details",
            "description": "Get details of a specific course. Anyone can access this endpoint.",
            "operationId": "getCourse",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the course to retrieve",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CourseDetail"}
                        }
                    }
                },
                "404": {"description": "Course not found"}
            }
        },
        "put": {
            "tags": ["Courses"],
            "summary": "Update course",
            "description": "Update a specific course. Only administrators can perform this action.",
            "operationId": "updateCourse",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the course to update",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/CourseCreate"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Course updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Course"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not an admin"},
                "404": {"description": "Course not found"}
            }
        },
        "patch": {
            "tags": ["Courses"],
            "summary": "Partially update course",
            "description": "Partially update a specific course. Only administrators can perform this action.",
            "operationId": "partialUpdateCourse",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the course to partially update",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/CoursePatch"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Course updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Course"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not an admin"},
                "404": {"description": "Course not found"}
            }
        },
        "delete": {
            "tags": ["Courses"],
            "summary": "Delete course",
            "description": "Delete a specific course. Only administrators can perform this action.",
            "operationId": "deleteCourse",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the course to delete",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "security": [{"Bearer": []}],
            "responses": {
                "204": {"description": "Course deleted successfully"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not an admin"},
                "404": {"description": "Course not found"}
            }
        }
    },
    "/courses/featured/": {
        "get": {
            "tags": ["Courses"],
            "summary": "List featured courses",
            "description": "Get a list of featured courses. Anyone can access this endpoint.",
            "operationId": "listFeaturedCourses",
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
                                        "items": {"$ref": "#/components/schemas/Course"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

# Course-related schemas for Swagger documentation
COURSE_COMPONENTS = {
    "Course": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "format": "int64",
                "readOnly": True
            },
            "title": {
                "type": "string",
                "example": "Introduction to Environmental Sustainability"
            },
            "description": {
                "type": "string",
                "example": "Learn the basics of environmental sustainability and how you can make a difference."
            },
            "instructor": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 5
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
            },
            "is_featured": {
                "type": "boolean",
                "example": True
            },
            "created_at": {
                "type": "string",
                "format": "date-time",
                "readOnly": True
            },
            "updated_at": {
                "type": "string",
                "format": "date-time",
                "readOnly": True
            },
            "enrollment_count": {
                "type": "integer",
                "readOnly": True,
                "example": 120
            }
        }
    },
    "CourseDetail": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "format": "int64",
                "readOnly": True
            },
            "title": {
                "type": "string",
                "example": "Introduction to Environmental Sustainability"
            },
            "description": {
                "type": "string",
                "example": "Learn the basics of environmental sustainability and how you can make a difference."
            },
            "instructor": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 5
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
            },
            "is_featured": {
                "type": "boolean",
                "example": True
            },
            "created_at": {
                "type": "string",
                "format": "date-time",
                "readOnly": True
            },
            "updated_at": {
                "type": "string",
                "format": "date-time",
                "readOnly": True
            },
            "enrollment_count": {
                "type": "integer",
                "readOnly": True,
                "example": 120
            }
        }
    },
    "CourseCreate": {
        "type": "object",
        "required": ["title", "description", "instructor_id", "duration", "level"],
        "properties": {
            "title": {
                "type": "string",
                "example": "Advanced Renewable Energy Systems"
            },
            "description": {
                "type": "string",
                "example": "Explore cutting-edge renewable energy technologies and implementation strategies."
            },
            "instructor_id": {
                "type": "integer",
                "example": 5,
                "description": "ID of an instructor (must be a staff user)"
            },
            "duration": {
                "type": "string",
                "example": "8 weeks"
            },
            "level": {
                "type": "string",
                "enum": ["BEG", "INT", "ADV"],
                "example": "ADV"
            },
            "is_featured": {
                "type": "boolean",
                "example": False
            }
        }
    },
    "CoursePatch": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "example": "Advanced Renewable Energy Systems"
            },
            "description": {
                "type": "string",
                "example": "Explore cutting-edge renewable energy technologies and implementation strategies."
            },
            "instructor_id": {
                "type": "integer",
                "example": 5,
                "description": "ID of an instructor (must be a staff user)"
            },
            "duration": {
                "type": "string",
                "example": "8 weeks"
            },
            "level": {
                "type": "string",
                "enum": ["BEG", "INT", "ADV"],
                "example": "ADV"
            },
            "is_featured": {
                "type": "boolean",
                "example": False
            }
        }
    }
}
