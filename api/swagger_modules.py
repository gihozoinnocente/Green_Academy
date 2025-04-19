"""
Module endpoints documentation for Swagger.
This module provides the OpenAPI spec for module-related endpoints.
"""

MODULE_PATHS = {
    "/modules/": {
        "get": {
            "tags": ["Modules"],
            "summary": "List all modules",
            "description": "Get a list of all modules for all courses.",
            "operationId": "listModules",
            "parameters": [
                {
                    "name": "course_id",
                    "in": "query",
                    "description": "Filter modules by course ID",
                    "required": False,
                    "schema": {"type": "integer"}
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
                                        "items": {"$ref": "#/components/schemas/Module"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["Modules"],
            "summary": "Create a new module",
            "description": "Create a new module for a course. Only instructors or admins can perform this action.",
            "operationId": "createModule",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ModuleCreate"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Module created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Module"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"}
            }
        }
    },
    "/modules/{id}/": {
        "get": {
            "tags": ["Modules"],
            "summary": "Retrieve module details",
            "description": "Get details of a specific module.",
            "operationId": "getModule",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the module to retrieve",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ModuleDetail"}
                        }
                    }
                },
                "404": {"description": "Module not found"}
            }
        },
        "put": {
            "tags": ["Modules"],
            "summary": "Update module",
            "description": "Update a specific module. Only instructors or admins can perform this action.",
            "operationId": "updateModule",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ModuleCreate"}
                    }
                }
            },
            "responses": {
                "200": {"description": "Module updated successfully"},
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"},
                "404": {"description": "Module not found"}
            }
        },
        "delete": {
            "tags": ["Modules"],
            "summary": "Delete module",
            "description": "Delete a specific module. Only instructors or admins can perform this action.",
            "operationId": "deleteModule",
            "security": [{"Bearer": []}],
            "responses": {
                "204": {"description": "Module deleted successfully"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"},
                "404": {"description": "Module not found"}
            }
        }
    }
}

MODULE_COMPONENTS = {
    "Module": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "readOnly": True},
            "course_id": {"type": "integer", "description": "ID of the course this module belongs to"},
            "title": {"type": "string", "example": "Module 1: Introduction"},
            "description": {"type": "string", "example": "Overview of the course and key concepts."}
        }
    },
    "ModuleDetail": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "readOnly": True},
            "course_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "activities": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/Activity"}
            }
        }
    },
    "ModuleCreate": {
        "type": "object",
        "required": ["course_id", "title", "description"],
        "properties": {
            "course_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"}
        }
    }
}
