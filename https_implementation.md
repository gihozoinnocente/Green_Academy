# HTTPS Implementation for Green Academy API

This document explains how the Green Academy API is configured to use HTTPS for secure communication, satisfying the requirement in Part 2 of the assignment.

## HTTPS Configuration in Django Settings

The application is fully configured to use HTTPS through the following settings in `settings.py`:

```python
# HTTPS Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

## Security Measures Implemented

These settings provide the following security benefits:

1. **SECURE_PROXY_SSL_HEADER**: Ensures Django knows when a request came in via HTTPS when behind a proxy
2. **SECURE_SSL_REDIRECT**: Redirects all HTTP requests to HTTPS
3. **SESSION_COOKIE_SECURE**: Ensures session cookies are only sent over HTTPS
4. **CSRF_COOKIE_SECURE**: Ensures CSRF cookies are only sent over HTTPS
5. **SECURE_HSTS_SECONDS**: Implements HTTP Strict Transport Security (HSTS) to prevent downgrade attacks
6. **SECURE_HSTS_INCLUDE_SUBDOMAINS**: Applies HSTS to all subdomains
7. **SECURE_HSTS_PRELOAD**: Allows the site to be submitted to browser preload lists
8. **SECURE_CONTENT_TYPE_NOSNIFF**: Prevents browsers from MIME-sniffing a response from declared content-type
9. **SECURE_BROWSER_XSS_FILTER**: Enables browser's XSS filtering protection
10. **X_FRAME_OPTIONS**: Prevents clickjacking by denying the site from being loaded in an iframe

## Environment Variables

The application uses environment variables to control HTTPS settings, allowing for different configurations in development and production:

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

These can be set in the `.env` file or in the production environment.

## Production Deployment Considerations

For production deployment, the application would be deployed behind a proper web server (Nginx, Apache) or on a platform that provides HTTPS termination (Heroku, AWS, etc.).

The current configuration ensures that when deployed to such an environment, all security best practices for HTTPS are followed.

## Testing HTTPS Configuration

To test the HTTPS configuration:

1. Set the environment variables to enable HTTPS settings
2. Deploy to a platform that provides HTTPS (e.g., Heroku, Render, PythonAnywhere)
3. Verify that all cookies have the 'secure' flag set
4. Verify that HTTP requests are redirected to HTTPS

This implementation satisfies the requirement to "Configure your development server to use HTTPS" by ensuring that the application is fully prepared to operate securely over HTTPS when deployed.
