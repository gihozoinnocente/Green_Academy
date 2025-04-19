# Green Academy API Design Document

## 1. Resources

The main resources for the Green Academy API are:

1. **Users** - Platform users (students, instructors, admins)
2. **Courses** - Educational content offered by Green Academy
3. **Enrollments** - Relationship between Users and Courses
4. **Modules** - Course sections or chapters
5. **Activities** - Learning activities within modules (lessons, quizzes, etc.)

For Phase 1, we will focus on implementing:
- Users
- Courses
- Enrollments

## 2. API Endpoints

### 2.1 Users

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/users/` | GET | List all users (admin only) |
| `/api/users/` | POST | Create a new user |
| `/api/users/{id}/` | GET | Retrieve details of a specific user |
| `/api/users/{id}/` | PUT/PATCH | Update a specific user |
| `/api/users/{id}/` | DELETE | Delete a specific user |
| `/api/users/me/` | GET | Retrieve the current authenticated user's details |

### 2.2 Courses

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/courses/` | GET | List all courses |
| `/api/courses/` | POST | Create a new course (admin only) |
| `/api/courses/{id}/` | GET | Retrieve details of a specific course |
| `/api/courses/{id}/` | PUT/PATCH | Update a specific course (admin only) |
| `/api/courses/{id}/` | DELETE | Delete a specific course (admin only) |
| `/api/courses/featured/` | GET | List featured courses |

### 2.3 Enrollments

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/api/enrollments/` | GET | List all enrollments (admin view) |
| `/api/enrollments/` | POST | Create a new enrollment |
| `/api/enrollments/{id}/` | GET | Retrieve a specific enrollment |
| `/api/enrollments/{id}/` | PUT/PATCH | Update a specific enrollment |
| `/api/enrollments/{id}/` | DELETE | Delete (unenroll) a specific enrollment |
| `/api/users/{id}/enrollments/` | GET | List enrollments for a specific user |
| `/api/courses/{id}/enrollments/` | GET | List enrollments for a specific course (admin only) |

## 3. Request/Response Structure

### 3.1 Users

#### GET /api/users/
**Response:**
```json
{
  "count": 50,
  "next": "http://greenacademy.org/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john.doe@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2023-01-15T08:30:00Z",
      "is_active": true,
      "is_staff": false
    },
    ...
  ]
}
```

#### POST /api/users/
**Request:**
```json
{
  "username": "newuser",
  "email": "new.user@example.com",
  "password": "securepassword123",
  "first_name": "New",
  "last_name": "User"
}
```

**Response:**
```json
{
  "id": 51,
  "username": "newuser",
  "email": "new.user@example.com",
  "first_name": "New",
  "last_name": "User",
  "date_joined": "2023-04-20T14:25:30Z",
  "is_active": true,
  "is_staff": false
}
```

### 3.2 Courses

#### GET /api/courses/
**Response:**
```json
{
  "count": 20,
  "next": "http://greenacademy.org/api/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Environmental Sustainability",
      "description": "Learn the basics of environmental sustainability and how you can make a difference.",
      "instructor": {
        "id": 5,
        "name": "Dr. Jane Smith"
      },
      "duration": "6 weeks",
      "level": "Beginner",
      "is_featured": true,
      "created_at": "2023-01-10T12:00:00Z",
      "updated_at": "2023-04-15T09:30:00Z",
      "enrollment_count": 120
    },
    ...
  ]
}
```

#### POST /api/courses/
**Request:**
```json
{
  "title": "Advanced Renewable Energy Systems",
  "description": "Explore cutting-edge renewable energy technologies and implementation strategies.",
  "instructor_id": 5,
  "duration": "8 weeks",
  "level": "Advanced",
  "is_featured": false
}
```

**Response:**
```json
{
  "id": 21,
  "title": "Advanced Renewable Energy Systems",
  "description": "Explore cutting-edge renewable energy technologies and implementation strategies.",
  "instructor": {
    "id": 5,
    "name": "Dr. Jane Smith"
  },
  "duration": "8 weeks",
  "level": "Advanced",
  "is_featured": false,
  "created_at": "2023-04-20T15:00:00Z",
  "updated_at": "2023-04-20T15:00:00Z",
  "enrollment_count": 0
}
```

### 3.3 Enrollments

#### GET /api/enrollments/
**Response:**
```json
{
  "count": 500,
  "next": "http://greenacademy.org/api/enrollments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 10,
        "username": "student1",
        "email": "student1@example.com"
      },
      "course": {
        "id": 5,
        "title": "Climate Change Fundamentals"
      },
      "enrolled_at": "2023-02-15T10:30:00Z",
      "status": "active",
      "completion_percentage": 65
    },
    ...
  ]
}
```

#### POST /api/enrollments/
**Request:**
```json
{
  "user_id": 10,
  "course_id": 8
}
```

**Response:**
```json
{
  "id": 501,
  "user": {
    "id": 10,
    "username": "student1",
    "email": "student1@example.com"
  },
  "course": {
    "id": 8,
    "title": "Sustainable Urban Development"
  },
  "enrolled_at": "2023-04-20T15:30:00Z",
  "status": "active",
  "completion_percentage": 0
}
```

## 4. Status Codes

| Status Code | Description | Example Scenario |
|-------------|-------------|-----------------|
| 200 OK | Request successful | GET request for a resource |
| 201 Created | Resource created successfully | POST request to create a new resource |
| 204 No Content | Request successful, no content returned | DELETE request |
| 400 Bad Request | Invalid request | Missing required fields or invalid data |
| 401 Unauthorized | Authentication required | Missing or invalid authentication token |
| 403 Forbidden | Authentication valid, but not authorized | Non-admin trying to access admin-only endpoint |
| 404 Not Found | Resource not found | Accessing non-existent resource |
| 405 Method Not Allowed | HTTP method not allowed for endpoint | Using POST on a GET-only endpoint |
| 429 Too Many Requests | Rate limit exceeded | Too many requests in a short time period |
| 500 Internal Server Error | Server error | Unexpected server-side error |

## 5. Pagination

For endpoints that return lists of resources, we will use **offset-based pagination** with the following parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10, max: 100)

Response structure for paginated results:
```json
{
  "count": 500,  // Total number of items
  "next": "http://greenacademy.org/api/resource/?page=3",  // URL to next page (null if no next page)
  "previous": "http://greenacademy.org/api/resource/?page=1",  // URL to previous page (null if no previous page)
  "results": [  // Array of items for the current page
    { ... },
    { ... }
  ]
}
```

## 6. Personal Data Handling

The API handles the following personal data:

- **User data**: names, email addresses, usernames, passwords
- **Learning progress data**: course progress, assessment results

### Data Protection Strategy:

1. **Authentication and Authorization**: 
   - JWT-based authentication for secure API access
   - Role-based permissions for different user types (student, instructor, admin)

2. **Data Security**:
   - Passwords are hashed using Django's built-in password hashing
   - HTTPS for all API communications
   - Personal data encrypted at rest in the database

3. **GDPR Compliance**:
   - User consent collection during registration
   - Data minimization (only collecting necessary data)
   - User data export endpoint for data portability
   - User data deletion endpoint for right to be forgotten

4. **Data Access and Audit**:
   - Logging of all actions involving personal data
   - Regular audits of personal data access

## 7. Caching Strategy

We will implement the following caching strategies:

1. **Course List Caching**:
   - Cache the list of featured courses for 1 hour using Django's cache framework
   - Invalidate cache when courses are updated/created/deleted

2. **Course Detail Caching**:
   - Cache individual course details for 6 hours
   - Invalidate cache when the specific course is updated

3. **User Enrollment Caching**:
   - Cache a user's enrollment list for 15 minutes
   - Invalidate cache when enrollments change for that user

We'll use Redis as our caching backend for its high performance, persistence capabilities, and support for complex data structures.

## 8. Authentication Methods

The Green Academy API implements two authentication methods to provide flexibility and security for different use cases:

### 8.1 JWT (JSON Web Token) Authentication

**Implementation Details:**
- Uses `djangorestframework-simplejwt` for token generation and validation
- Access tokens expire after 1 hour
- Refresh tokens expire after 7 days
- Tokens are signed with HS256 algorithm using a secure secret key

**Use Cases:**
- Primary authentication method for most API clients
- Mobile applications and single-page applications (SPAs)
- Third-party integrations requiring programmatic access
- Any scenario where stateless authentication is preferred

**Endpoints:**
- `/api/token/` - Obtain JWT token pair (access and refresh tokens)
- `/api/token/refresh/` - Refresh access token
- `/api/token/verify/` - Verify token validity

### 8.2 Basic Authentication

**Implementation Details:**
- Uses Django REST Framework's BasicAuthentication class
- Requires HTTPS to ensure credentials are encrypted during transmission
- Only enabled for specific admin endpoints

**Use Cases:**
- Admin-specific functionalities requiring higher security
- Emergency access when JWT infrastructure is unavailable
- Command-line tools and scripts for administrative tasks
- Development and debugging environments

**Security Considerations:**
- Only available over HTTPS to prevent credential interception
- Rate-limited to prevent brute force attacks
- Logs all access attempts for security auditing

## 9. Authorization (Granular Control)

### 9.1 Role Definitions

| Role | Description |
|------|-------------|
| **Student** | Regular users who can enroll in courses and access learning materials |
| **Instructor** | Users who can create and manage their own courses and monitor student progress |
| **Admin** | Users with full system access for platform management |
| **Content Manager** | Users who can review and approve course content but cannot modify user data |
| **Support Staff** | Users who can view limited user data to provide customer support |

### 9.2 Permission Mapping

| Endpoint | Student | Instructor | Content Manager | Support Staff | Admin |
|----------|---------|------------|-----------------|--------------|-------|
| `GET /api/users/` | ❌ | ❌ | ❌ | ✅ (limited) | ✅ |
| `POST /api/users/` | ✅ (self) | ✅ (self) | ❌ | ❌ | ✅ |
| `GET /api/users/{id}/` | ✅ (self) | ✅ (self) | ❌ | ✅ | ✅ |
| `PUT/PATCH /api/users/{id}/` | ✅ (self) | ✅ (self) | ❌ | ❌ | ✅ |
| `DELETE /api/users/{id}/` | ❌ | ❌ | ❌ | ❌ | ✅ |
| `GET /api/courses/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `POST /api/courses/` | ❌ | ✅ (own) | ❌ | ❌ | ✅ |
| `GET /api/courses/{id}/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `PUT/PATCH /api/courses/{id}/` | ❌ | ✅ (own) | ✅ | ❌ | ✅ |
| `DELETE /api/courses/{id}/` | ❌ | ✅ (own) | ❌ | ❌ | ✅ |
| `GET /api/enrollments/` | ✅ (own) | ✅ (own courses) | ❌ | ✅ | ✅ |
| `POST /api/enrollments/` | ✅ (self) | ❌ | ❌ | ✅ | ✅ |
| `DELETE /api/enrollments/{id}/` | ✅ (own) | ❌ | ❌ | ✅ | ✅ |

### 9.3 Implementation Approach

**Role-Based Access Control (RBAC):**
- Implemented using Django's built-in permissions system
- Extended with custom permission classes in Django REST Framework
- User roles stored in the database with a many-to-many relationship to permissions

**Object-Level Permissions:**
- Instructors can only modify their own courses
- Students can only view their own enrollment and progress data
- Support staff can view but not modify user data

**Example Implementation:**

```python
class IsCourseInstructorOrReadOnly(permissions.BasePermission):
    """Allow course instructors to edit their own courses."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions only for the course instructor
        return obj.instructor == request.user
```

## 10. Sensitive Data Handling

### 10.1 Password Storage

- Passwords are hashed using Django's built-in password hasher (PBKDF2 with SHA256)
- Password hashing uses a minimum of 320,000 iterations (Django's default as of 2023)
- Each password is stored with a unique salt to prevent rainbow table attacks
- Password reset tokens are short-lived (valid for 24 hours)

### 10.2 API Keys and Secrets

- JWT secret keys are stored as environment variables, not in the codebase
- All API keys for third-party services are stored in environment variables
- Production secrets are managed using a secure vault service (HashiCorp Vault)
- Different keys are used for development, staging, and production environments

### 10.3 Environment Variables

- Environment variables are loaded using python-dotenv or Django's built-in env management
- Production environment variables are managed through the deployment platform (e.g., AWS Parameter Store)
- Example environment variables structure:

```
DJANGO_SECRET_KEY=<random-string>
JWT_SECRET_KEY=<random-string>
DATABASE_URL=postgres://user:password@host:port/db
REDIS_URL=redis://host:port/db
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
```

### 10.4 Database Security

- Database credentials are never hardcoded in the codebase
- Production database is encrypted at rest
- Database connections use SSL/TLS encryption
- Regular security audits and vulnerability assessments

## 11. Input Validation

### 11.1 Validation Techniques

**Django REST Framework Serializers:**
- Primary method for validating API input
- Field-level validation with built-in validators
- Custom validation methods for complex business rules

**Example Serializer with Validation:**

```python
class CourseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=Course.objects.all())])
    description = serializers.CharField(max_length=1000)
    level = serializers.ChoiceField(choices=['Beginner', 'Intermediate', 'Advanced'])
    
    def validate_description(self, value):
        """Ensure description doesn't contain HTML tags."""
        if re.search('<[^>]*>', value):
            raise serializers.ValidationError("Description cannot contain HTML tags")
        return value
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'duration', 'level', 'is_featured']
```

### 11.2 SQL Injection Prevention

- Django's ORM provides protection against SQL injection by default
- Raw SQL queries are avoided when possible
- When raw SQL is necessary, it uses parameterized queries
- Regular security audits to identify potential vulnerabilities

### 11.3 Cross-Site Scripting (XSS) Prevention

- Input sanitization to remove potentially malicious content
- Content-Security-Policy headers to restrict script execution
- Django's built-in XSS protection with auto-escaping in templates
- Output encoding when displaying user-generated content

### 11.4 Additional Security Measures

- CSRF protection for all non-GET requests
- Rate limiting to prevent brute force attacks
- Input size limits to prevent denial of service attacks
- Regular security training for development team

## 12. Error Handling

### 12.1 Error Response Structure

All API error responses follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### 12.2 Common Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `AUTHENTICATION_FAILED` | 401 | Invalid or missing authentication credentials |
| `PERMISSION_DENIED` | 403 | User does not have permission for this action |
| `RESOURCE_NOT_FOUND` | 404 | The requested resource does not exist |
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests in a given time period |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### 12.3 Security Considerations

- Error messages never reveal sensitive information (e.g., database details, stack traces)
- Generic error messages for security-related failures (e.g., "Invalid credentials" instead of "User not found")
- Detailed error logging for debugging, but only accessible to authorized personnel
- Different error verbosity for development and production environments

### 12.4 Implementation Example

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_code = 'UNKNOWN_ERROR'
        
        if response.status_code == 401:
            error_code = 'AUTHENTICATION_FAILED'
        elif response.status_code == 403:
            error_code = 'PERMISSION_DENIED'
        elif response.status_code == 404:
            error_code = 'RESOURCE_NOT_FOUND'
        elif response.status_code == 400:
            error_code = 'VALIDATION_ERROR'
        
        response.data = {
            'error': {
                'code': error_code,
                'message': str(exc),
                'details': response.data if hasattr(response, 'data') else {}
            }
        }
    
    return response
```

## 13. API Documentation

### 13.1 Automatic Documentation Generation

The Green Academy API uses **drf-yasg** (Yet Another Swagger Generator) to automatically generate comprehensive API documentation from the codebase. This provides:

- Interactive Swagger UI for exploring the API
- OpenAPI 3.0 specification document
- Ability to test API endpoints directly from the documentation

### 13.2 Documentation Content

The automatically generated documentation includes:

- Complete list of all API endpoints
- Required and optional parameters for each endpoint
- Request body schemas with field descriptions
- Response schemas with examples
- Authentication requirements
- Error codes and descriptions
- Pagination information

### 13.3 Documentation Enhancement

To enhance the automatically generated documentation, we use:

- Detailed docstrings in views and serializers
- Custom schema generation for complex endpoints
- Manual descriptions for parameters and fields
- Example requests and responses

**Example View with Enhanced Documentation:**

```python
class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing courses.
    
    Courses represent educational content offered by Green Academy.
    Only instructors can create courses, and they can only modify their own courses.
    Admins have full access to all courses.
    """
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCourseInstructorOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="List all available courses",
        responses={200: CourseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

### 13.4 Documentation Access

API documentation is available at the following endpoints:

- Swagger UI: `/swagger/`
- ReDoc UI (alternative documentation view): `/redoc/`
- OpenAPI schema: `/swagger.json` or `/swagger.yaml`

Access to the documentation in production is restricted to authenticated users to prevent information disclosure to unauthorized parties.