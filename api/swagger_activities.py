"""
Activity endpoints documentation for Swagger.
This module provides the OpenAPI spec for activity-related endpoints.
"""

ACTIVITY_PATHS = {
    "/activities/": {
        "get": {
            "tags": ["Activities"],
            "summary": "List all activities",
            "description": "Get a list of all activities for all modules.",
            "operationId": "listActivities",
            "parameters": [
                {
                    "name": "module_id",
                    "in": "query",
                    "description": "Filter activities by module ID",
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
                                        "items": {"$ref": "#/components/schemas/Activity"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "post": {
            "tags": ["Activities"],
            "summary": "Create a new activity",
            "description": "Create a new activity for a module. Only instructors or admins can perform this action.",
            "operationId": "createActivity",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ActivityCreate"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Activity created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Activity"}
                        }
                    }
                },
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"}
            }
        }
    },
    "/activities/{id}/": {
        "get": {
            "tags": ["Activities"],
            "summary": "Retrieve activity details",
            "description": "Get details of a specific activity.",
            "operationId": "getActivity",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "description": "ID of the activity to retrieve",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ],
            "responses": {
                "200": {
                    "description": "Successful operation",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ActivityDetail"}
                        }
                    }
                },
                "404": {"description": "Activity not found"}
            }
        },
        "put": {
            "tags": ["Activities"],
            "summary": "Update activity",
            "description": "Update a specific activity. Only instructors or admins can perform this action.",
            "operationId": "updateActivity",
            "security": [{"Bearer": []}],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ActivityCreate"}
                    }
                }
            },
            "responses": {
                "200": {"description": "Activity updated successfully"},
                "400": {"description": "Bad request - Invalid input"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"},
                "404": {"description": "Activity not found"}
            }
        },
        "delete": {
            "tags": ["Activities"],
            "summary": "Delete activity",
            "description": "Delete a specific activity. Only instructors or admins can perform this action.",
            "operationId": "deleteActivity",
            "security": [{"Bearer": []}],
            "responses": {
                "204": {"description": "Activity deleted successfully"},
                "401": {"description": "Authentication required"},
                "403": {"description": "Forbidden - not allowed"},
                "404": {"description": "Activity not found"}
            }
        }
    }
}

ACTIVITY_COMPONENTS = {
    "Activity": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "readOnly": True},
            "module_id": {"type": "integer", "description": "ID of the module this activity belongs to"},
            "title": {"type": "string", "example": "Lesson 1: What is Sustainability?"},
            "description": {"type": "string", "example": "Introduction to sustainability concepts."},
            "type": {"type": "string", "enum": ["lesson", "quiz", "assignment"], "example": "lesson"}
        }
    },
    "ActivityDetail": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "readOnly": True},
            "module_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "type": {"type": "string", "enum": ["lesson", "quiz", "assignment"]}
        }
    },
    "ActivityCreate": {
        "type": "object",
        "required": ["module_id", "title", "description", "type"],
        "properties": {
            "module_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "type": {"type": "string", "enum": ["lesson", "quiz", "assignment"]}
        }
    }
}
