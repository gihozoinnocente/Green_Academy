# Green Academy API

The Green Academy API provides backend services for an online learning platform focused on environmental sustainability and conservation education. This repository contains the Phase 1 implementation which focuses on courses and student enrollment.

## Features

- User management (authentication, authorization)
- Course management (create, read, update, delete)
- Enrollment management
- Type-checked Python code with mypy
- Paginated API responses
- Caching for improved performance

## Technology Stack

- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis (for caching)
- JWT Authentication

## Prerequisites

- Python 3.10 or higher
- PostgreSQL
- Redis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/green-academy-api.git
cd green-academy-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/green_academy
REDIS_URL=redis://localhost:6379/1
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/api/

## API Documentation

API documentation is available at:
- API endpoints: http://127.0.0.1:8000/swagger/
- API design document: See [API_DESIGN.md](API_DESIGN.md) for detailed information
- Privacy Statement: See [privacy_statement.md](privacy_statement.md) for our privacy policy
- Permissions Documentation: See [permissions_documentation.md](permissions_documentation.md) for detailed information about the API's permission system

## Type Checking with Mypy

To run static type checking with mypy:
```bash
mypy .
```

## Running Tests

To run the test suite:
```bash
python manage.py test tests
```

## Deployment

### Platform Selection: Railway

**Justification for choosing Railway:**

1. **Ease of Use**: Railway offers a straightforward deployment process with minimal configuration, making it ideal for Django applications.

2. **PostgreSQL Support**: Railway provides managed PostgreSQL databases that integrate seamlessly with Django applications.

3. **Redis Support**: Built-in Redis service for our caching requirements.

4. **CI/CD Integration**: Automatic deployments from GitHub repositories.

5. **HTTPS by Default**: Railway provides SSL certificates automatically.

6. **Reasonable Free Tier**: Offers a free tier suitable for demonstration purposes.

7. **Scalability**: Easy to scale as the application grows.

### Deployment Steps

#### 1. Prepare the Application for Deployment

1. Ensure your code is in a GitHub repository.

2. Add a `Procfile` to the project root:
   ```
   web: gunicorn green_academy.wsgi --log-file -
   ```

3. Update `requirements.txt` to include deployment dependencies:
   ```bash
   pip install gunicorn dj-database-url whitenoise psycopg2-binary
   pip freeze > requirements.txt
   ```

4. Configure static files in `settings.py`:
   ```python
   # Add 'whitenoise.middleware.WhiteNoiseMiddleware' after SecurityMiddleware
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',
       # other middleware...
   ]
   
   # Configure static files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATIC_URL = '/static/'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

5. Create a `runtime.txt` file specifying the Python version:
   ```
   python-3.10.x
   ```

#### 2. Deploy to Railway

1. Create a Railway account at [railway.app](https://railway.app)

2. Install the Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

3. Login to Railway:
   ```bash
   railway login
   ```

4. Create a new project:
   ```bash
   railway init
   ```

5. Add PostgreSQL and Redis services:
   ```bash
   railway add
   # Select PostgreSQL from the menu
   railway add
   # Select Redis from the menu
   ```

6. Configure environment variables:
   ```bash
   railway variables --set "DEBUG=False"
   railway variables --set "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
   railway variables --set "ALLOWED_HOSTS=your-app-domain.railway.app"
   railway variables --set "SECURE_SSL_REDIRECT=True"
   railway variables --set "SESSION_COOKIE_SECURE=True"
   railway variables --set "CSRF_COOKIE_SECURE=True"
   ```

7. Deploy the application:
   ```bash
   railway up
   ```

8. Run migrations on the production database:
   ```bash
   railway run python manage.py migrate
   ```

9. Create a superuser for the production environment:
   ```bash
   railway run python manage.py createsuperuser
   ```

10. Access your deployed application:
    ```bash
    railway open
    ```

#### 3. Continuous Deployment

1. Connect your GitHub repository to Railway:
   - Go to your Railway project dashboard
   - Click on "Settings"
   - Under "Source", connect to your GitHub repository
   - Select the branch to deploy (usually `main` or `master`)

2. Configure automatic deployments:
   - Enable "Automatic Deployments" in the Railway dashboard
   - Railway will now automatically deploy when changes are pushed to the selected branch

#### 4. Monitoring and Maintenance

1. View application logs:
   ```bash
   railway logs
   ```

2. Monitor application performance in the Railway dashboard.

3. Update your application:
   - Push changes to your GitHub repository
   - Railway will automatically deploy the updates

4. Scale your application as needed through the Railway dashboard.

## Secure Configuration Management

### Environment Variables Strategy

The Green Academy API follows security best practices by using environment variables for all sensitive configuration. This approach ensures that sensitive information is never stored in the codebase.

#### Local Development

For local development, we use a `.env` file that is explicitly excluded from version control via `.gitignore`. This file should contain:

```
DEBUG=True
SECRET_KEY=your-local-development-key
DATABASE_URL=postgres://user:password@localhost:5432/green_academy
REDIS_URL=redis://localhost:6379/1
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Production Environment

In production, environment variables are set through the Railway dashboard or CLI, never stored in files:

```bash
railway variables --set "DEBUG=False"
railway variables --set "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
railway variables --set "ALLOWED_HOSTS=your-app-domain.railway.app"
railway variables --set "SECURE_SSL_REDIRECT=True"
railway variables --set "SESSION_COOKIE_SECURE=True"
railway variables --set "CSRF_COOKIE_SECURE=True"
```

### Database Security

1. **Connection Pooling**: The application uses connection pooling to efficiently manage database connections.

2. **Parameterized Queries**: All database queries use Django's ORM with parameterized queries to prevent SQL injection.

3. **Limited Privileges**: The database user has only the necessary privileges required for the application to function.

4. **Encrypted Connections**: Database connections use SSL/TLS encryption in production.

### Secret Management

1. **Secret Rotation**: Production secrets are rotated regularly (every 90 days).

2. **Secret Access Control**: Access to production secrets is strictly limited to DevOps personnel.

3. **No Hardcoded Secrets**: The codebase is regularly scanned to ensure no secrets are hardcoded.

## Monitoring Strategy

The Green Academy API implements a comprehensive monitoring strategy to ensure high availability, performance, and security.

### Application Performance Monitoring

1. **Sentry Integration**

   We use Sentry for error tracking and performance monitoring:
   
   ```python
   # Add to settings.py
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   
   if not DEBUG and os.environ.get('SENTRY_DSN'):
       sentry_sdk.init(
           dsn=os.environ.get('SENTRY_DSN'),
           integrations=[DjangoIntegration()],
           traces_sample_rate=0.5,
           send_default_pii=False
       )
   ```

2. **Prometheus Metrics**

   We expose application metrics using the django-prometheus package:
   
   ```python
   # Add to INSTALLED_APPS in settings.py
   INSTALLED_APPS = [
       # ...
       'django_prometheus',
       # ...
   ]
   
   # Add to MIDDLEWARE in settings.py (at the beginning and end)
   MIDDLEWARE = [
       'django_prometheus.middleware.PrometheusBeforeMiddleware',
       # ... existing middleware
       'django_prometheus.middleware.PrometheusAfterMiddleware',
   ]
   ```

### Health Checks

We implement health check endpoints to monitor system components:

```python
# Add to urls.py
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import RedisError
import redis

def health_check(request):
    # Check database connection
    try:
        connections['default'].cursor()
        db_status = True
    except OperationalError:
        db_status = False
    
    # Check Redis connection
    try:
        redis_client = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/1'))
        redis_client.ping()
        redis_status = True
    except RedisError:
        redis_status = False
    
    status = db_status and redis_status
    status_code = 200 if status else 503
    
    response = {
        'status': 'healthy' if status else 'unhealthy',
        'components': {
            'database': 'up' if db_status else 'down',
            'redis': 'up' if redis_status else 'down',
        }
    }
    
    return JsonResponse(response, status=status_code)

# In urlpatterns
path('health/', health_check, name='health_check'),
```

### Log Management

1. **Structured Logging**

   We use structured logging with Python's logging module and JSON formatting:
   
   ```python
   # Add to settings.py
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'json': {
               'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
               'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
           },
       },
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
               'formatter': 'json',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['console'],
               'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
           },
           'api': {
               'handlers': ['console'],
               'level': os.getenv('API_LOG_LEVEL', 'INFO'),
           },
       },
   }
   ```

2. **Log Aggregation**

   In production, logs are aggregated using Railway's built-in log management or forwarded to a dedicated log management service like Datadog or Logz.io.

### Security Monitoring

1. **Dependency Scanning**: Regular automated scanning of dependencies for security vulnerabilities using tools like Safety or Snyk.

2. **Rate Limiting**: Implementation of rate limiting to prevent abuse:

   ```python
   # Add to settings.py
   REST_FRAMEWORK = {
       # ... existing settings
       'DEFAULT_THROTTLE_CLASSES': [
           'rest_framework.throttling.AnonRateThrottle',
           'rest_framework.throttling.UserRateThrottle'
       ],
       'DEFAULT_THROTTLE_RATES': {
           'anon': '100/day',
           'user': '1000/day'
       }
   }
   ```

3. **Failed Login Monitoring**: Tracking and alerting on multiple failed login attempts.

### Alerting Strategy

1. **Alert Thresholds**: Alerts are configured for:
   - Error rate exceeding normal baseline
   - API response time degradation
   - Database connection failures
   - Redis connection failures
   - High CPU/memory usage
   - Unusual traffic patterns

2. **On-Call Rotation**: A defined on-call schedule ensures timely response to alerts.

3. **Incident Response Plan**: A documented incident response plan outlines steps to take when alerts are triggered.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests and type checking
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
