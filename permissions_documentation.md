# Green Academy API - Permissions and Authentication Documentation

This document provides a comprehensive overview of the permissions and authentication requirements for all endpoints in the Green Academy API.

## Authentication

The Green Academy API uses JWT (JSON Web Token) for authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api/auth/login/` with your username/email and password
2. Include the token in the Authorization header of your requests: `Authorization: Bearer <your_token>`

## User Roles

The API has three main user roles:

- **Student**: Regular users who can enroll in courses and access learning materials
- **Instructor**: Users who can create and manage courses, modules, and activities
- **Admin**: Users with full access to all API endpoints

## Endpoints and Permissions

### Authentication Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/auth/login/` | POST | Obtain JWT token | No | Any |
| `/api/auth/refresh/` | POST | Refresh JWT token | No | Any |
| `/api/auth/verify/` | POST | Verify JWT token | No | Any |

### User Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/users/` | GET | List all users | Yes | Admin |
| `/api/users/` | POST | Create a new user | No | Any |
| `/api/users/{id}/` | GET | Retrieve user details | Yes | Owner or Admin |
| `/api/users/{id}/` | PUT | Update user | Yes | Owner or Admin |
| `/api/users/{id}/` | PATCH | Partially update user | Yes | Owner or Admin |
| `/api/users/{id}/` | DELETE | Delete user | Yes | Owner or Admin |
| `/api/users/me/` | GET | Get current user | Yes | Any authenticated user |
| `/api/users/me/export/` | GET | Export personal data | Yes | Any authenticated user |
| `/api/users/me/delete/` | DELETE | Delete own account | Yes | Any authenticated user |
| `/api/users/{id}/enrollments/` | GET | List user enrollments | Yes | Owner or Admin |

### Course Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/courses/` | GET | List all courses | No | Any |
| `/api/courses/` | POST | Create a new course | Yes | Admin |
| `/api/courses/{id}/` | GET | Retrieve course details | No | Any |
| `/api/courses/{id}/` | PUT | Update course | Yes | Admin |
| `/api/courses/{id}/` | PATCH | Partially update course | Yes | Admin |
| `/api/courses/{id}/` | DELETE | Delete course | Yes | Admin |
| `/api/courses/featured/` | GET | List featured courses | No | Any |
| `/api/courses/{id}/enrollments/` | GET | List course enrollments | Yes | Admin |

### Enrollment Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/enrollments/` | GET | List all enrollments | Yes | Admin (all), User (own) |
| `/api/enrollments/` | POST | Create a new enrollment | Yes | Any authenticated user |
| `/api/enrollments/{id}/` | GET | Retrieve enrollment details | Yes | Owner or Admin |
| `/api/enrollments/{id}/` | PUT | Update enrollment | Yes | Owner or Admin |
| `/api/enrollments/{id}/` | PATCH | Partially update enrollment | Yes | Owner or Admin |
| `/api/enrollments/{id}/` | DELETE | Delete enrollment | Yes | Owner or Admin |

### Module Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/modules/` | GET | List all modules | No | Any |
| `/api/modules/?course_id={id}` | GET | List modules for a course | No | Any |
| `/api/modules/` | POST | Create a new module | Yes | Any authenticated user |
| `/api/modules/{id}/` | GET | Retrieve module details | No | Any |
| `/api/modules/{id}/` | PUT | Update module | Yes | Any authenticated user |
| `/api/modules/{id}/` | PATCH | Partially update module | Yes | Any authenticated user |
| `/api/modules/{id}/` | DELETE | Delete module | Yes | Any authenticated user |

### Activity Endpoints

| Endpoint | Method | Description | Authentication Required | Roles Allowed |
|----------|--------|-------------|------------------------|---------------|
| `/api/activities/` | GET | List all activities | No | Any |
| `/api/activities/?module_id={id}` | GET | List activities for a module | No | Any |
| `/api/activities/` | POST | Create a new activity | Yes | Any authenticated user |
| `/api/activities/{id}/` | GET | Retrieve activity details | No | Any |
| `/api/activities/{id}/` | PUT | Update activity | Yes | Any authenticated user |
| `/api/activities/{id}/` | PATCH | Partially update activity | Yes | Any authenticated user |
| `/api/activities/{id}/` | DELETE | Delete activity | Yes | Any authenticated user |

## Permission Details

### IsOwnerOrAdmin

This permission allows:
- The owner of a resource (e.g., a user accessing their own data)
- Admin users

### IsEnrolledOrAdmin

This permission allows:
- Users enrolled in a specific course
- Admin users

### AllowAny

This permission allows any user, authenticated or not, to access the endpoint.

### IsAuthenticated

This permission requires the user to be authenticated but doesn't check for specific roles.

### IsAdminUser

This permission only allows admin users to access the endpoint.


## Error Responses

When authentication or permission checks fail, the API will respond with appropriate HTTP status codes:

- **401 Unauthorized**: Authentication is required but was not provided or is invalid
- **403 Forbidden**: Authentication succeeded, but the user doesn't have permission to access the resource
- **404 Not Found**: The requested resource doesn't exist
