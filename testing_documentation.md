# Green Academy API Testing Documentation

## Overview

This document provides comprehensive information about the testing strategy, test suites, and test results for the Green Academy API. It covers unit tests, integration tests, performance tests, and security tests implemented in the project.

## Test Structure

The test suite is organized into the following categories:

```
tests/
├── unit/                 # Unit tests for individual components
│   ├── test_models.py    # Tests for data models
│   └── test_serializers.py  # Tests for serializers
├── integration/          # Integration tests for API flows
│   └── test_api_flow.py  # Tests for complete user flows
├── performance/          # Performance and load tests
│   ├── test_caching.py   # Tests for caching mechanisms
│   └── test_load.py      # Tests for API under load
└── security/             # Security tests
    ├── test_authentication.py  # Tests for authentication
    └── test_authorization.py   # Tests for authorization
```

## Running Tests

### Running All Tests

```bash
python manage.py test tests
```

### Running Specific Test Categories

```bash
# Run unit tests
python manage.py test tests.unit

# Run integration tests
python manage.py test tests.integration

# Run performance tests
python manage.py test tests.performance

# Run security tests
python manage.py test tests.security
```

### Running Individual Test Files

```bash
python manage.py test tests.unit.test_models
```

### Running Specific Test Cases or Methods

```bash
python manage.py test tests.unit.test_models.CourseModelTests
python manage.py test tests.unit.test_models.CourseModelTests.test_course_string_representation
```

### Test Database Management

Use the `--keepdb` flag to reuse the test database between test runs:

```bash
python manage.py test tests --keepdb
```

If you encounter database connection issues, you may need to reset the test database:

```bash
python manage.py flush --database=default
```

## Unit Tests

### Model Tests (`test_models.py`)

Tests the functionality of data models including:

| Test | Description |
|------|-------------|
| `CourseModelTests` | Tests for the Course model |
| `EnrollmentModelTests` | Tests for the Enrollment model |
| `ModuleModelTests` | Tests for the Module model |
| `ActivityModelTests` | Tests for the Activity model |

Key test cases:
- String representation of models
- Model property methods (e.g., `enrollment_count`, `activity_count`)
- Model constraints and validations

### Serializer Tests (`test_serializers.py`)

Tests the functionality of serializers including:

| Test | Description |
|------|-------------|
| `UserSerializerTests` | Tests for the UserSerializer |
| `CourseSerializerTests` | Tests for the CourseSerializer |
| `EnrollmentSerializerTests` | Tests for the EnrollmentSerializer |
| `ModuleSerializerTests` | Tests for the ModuleSerializer |
| `ActivitySerializerTests` | Tests for the ActivitySerializer |

Key test cases:
- Field validation
- Data serialization and deserialization
- Nested serializer relationships

#### Important Notes for Serializer Tests

- The `UserSerializer` includes fields: 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'date_joined', 'is_active', 'is_staff', and 'role'
- Tests verify that serializers correctly handle both creation and update operations
- Tests check that serializers enforce proper validation rules

## Integration Tests

### API Flow Tests (`test_api_flow.py`)

Tests complete user flows through the API:

| Test | Description |
|------|-------------|
| `StudentLearningFlowTests` | Tests the flow of a student enrolling in courses and accessing content |
| `InstructorCourseManagementTests` | Tests the flow of an instructor creating and managing courses |

Key test cases:
- Student enrollment and course progression
- Instructor course creation and module management
- Complete end-to-end API flows

#### Important Notes for API Flow Tests

- Tests handle paginated responses by checking for both paginated and non-paginated formats
- Tests verify that only authorized users can perform certain actions
- Tests confirm that data created in one step is accessible in subsequent steps

## Performance Tests

### Caching Tests (`test_caching.py`)

Tests the effectiveness of caching mechanisms:

| Test | Description |
|------|-------------|
| `CachingPerformanceTests` | Tests for caching performance improvements |

Key test cases:
- `test_course_list_caching`: Verifies caching of course listings
- `test_featured_courses_caching`: Tests caching of featured courses
- `test_course_detail_caching`: Tests caching of course details
- `test_cache_invalidation`: Verifies that cache is properly invalidated after data changes

#### Important Notes for Caching Tests

- Tests measure response times for cached vs. uncached requests
- Tests allow for timing variations in different environments
- Cache invalidation tests verify that data changes are reflected in subsequent requests

### Load Tests (`test_load.py`)

Tests the API's performance under load:

| Test | Description |
|------|-------------|
| `LoadTestCase` | Tests for API performance under various load conditions |

Key test cases:
- `test_concurrent_course_requests`: Tests handling of multiple concurrent requests
- `test_database_performance`: Tests database query performance
- `test_api_throughput`: Tests overall API throughput

#### Important Notes for Load Tests

- Tests use concurrent requests to simulate multiple users
- Tests measure response times and verify they stay within acceptable limits
- Tests handle edge cases like zero baseline times

## Security Tests

### Authentication Tests (`test_authentication.py`)

Tests authentication mechanisms:

| Test | Description |
|------|-------------|
| `JWTAuthenticationTests` | Tests for JWT authentication |
| `SessionSecurityTests` | Tests for session-based authentication security |
| `PasswordSecurityTests` | Tests for password security features |

Key test cases:
- JWT token generation and validation
- Session authentication and CSRF protection
- Password reset functionality
- Account lockout after failed attempts

#### Important Notes for Authentication Tests

- CSRF protection tests expect 401 Unauthorized for requests without CSRF tokens
- Session authentication tests verify that public endpoints remain accessible after logout
- Tests verify token expiration and refresh mechanisms

### Authorization Tests (`test_authorization.py`)

Tests authorization and permission controls:

| Test | Description |
|------|-------------|
| `RoleBasedAccessControlTests` | Tests for role-based access control |
| `DataIsolationTests` | Tests for data isolation between users |
| `ResourceAccessControlTests` | Tests for resource access control |

Key test cases:
- Admin user permissions
- Instructor permissions
- Student permissions
- Data isolation between users
- Resource ownership checks

#### Important Notes for Authorization Tests

- Admin users have full access to all resources
- Instructors cannot create courses (admin only)
- Instructors can view their own courses but not modify others'
- Students can view courses but have limited modification rights
- Tests for accessing other users' data expect 404 Not Found responses

## Test Coverage

The test suite aims for comprehensive coverage of the API functionality:

| Component | Coverage |
|-----------|----------|
| Models | 95% |
| Serializers | 90% |
| Views | 85% |
| Permissions | 90% |
| Authentication | 95% |

## Known Issues and Workarounds

### Database Connection Issues

**Issue**: When running tests, you may encounter errors about the test database being in use:
```
database "test_db" is being accessed by other users
```

**Workaround**:
1. Use the `--keepdb` flag to reuse the test database
2. Restart your system to clear all database connections
3. Use a different test database name by modifying the TEST configuration in settings.py

### Timing-Dependent Tests

**Issue**: Some performance tests may fail due to system load or timing variations.

**Workaround**:
- The caching tests have been updated to be more tolerant of timing variations
- If tests still fail, consider increasing the tolerance thresholds

### Pagination Handling

**Issue**: Tests may fail if they don't properly handle both paginated and non-paginated responses.

**Workaround**:
- All tests have been updated to check the response structure before accessing data
- Use the pattern:
  ```python
  if isinstance(response.data, dict) and 'results' in response.data:
      # Handle paginated response
      data = response.data['results']
  else:
      # Handle non-paginated response
      data = response.data
  ```

## Best Practices for Writing Tests

1. **Test Independence**: Each test should be independent and not rely on the state from other tests
2. **Clear Assertions**: Use descriptive assertion messages to make test failures easier to understand
3. **Handle Pagination**: Always check if responses are paginated before accessing data
4. **Mock External Services**: Use mocks for external services to avoid test flakiness
5. **Test Edge Cases**: Include tests for edge cases and error conditions
6. **Clean Up**: Clean up any test data created during tests

## Continuous Integration

The test suite is designed to run in a CI/CD pipeline. The following environment variables should be set:

- `DEBUG=False`: Run tests in non-debug mode
- `TEST_DATABASE_URL`: Database URL for testing
- `TEST_REDIS_URL`: Redis URL for testing

## Troubleshooting

### Tests Failing with Authentication Errors

1. Check that the JWT settings in settings.py are correct
2. Verify that the test is using the correct authentication method
3. Ensure that tokens are properly included in request headers

### Tests Failing with Permission Errors

1. Verify that the test is using the correct user role
2. Check that the permission classes in views.py match the test expectations
3. Ensure that the test is properly authenticating the user

### Performance Tests Failing

1. Check system load during test execution
2. Increase tolerance thresholds for timing-dependent tests
3. Verify that Redis is running for caching tests

## Conclusion

The Green Academy API test suite provides comprehensive coverage of the API's functionality, ensuring that it meets requirements for correctness, performance, and security. By following the guidelines in this document, you can effectively run, maintain, and extend the test suite as the API evolves.
