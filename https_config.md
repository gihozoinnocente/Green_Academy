# Setting Up HTTPS for Development

This document explains how to set up HTTPS for your Django development environment to meet the security requirements in Part 2 of the assignment.

## Option 1: Using a Reverse Proxy (Recommended for Windows)

The most reliable way to set up HTTPS for development on Windows is to use a reverse proxy like Caddy, which automatically handles SSL certificates.

1. **Install Caddy Server**:
   - Download Caddy from [caddyserver.com](https://caddyserver.com/download)
   - Extract the executable to a location on your PATH

2. **Create a Caddyfile**:
   - Create a file named `Caddyfile` (no extension) in the project root with the following content:
   ```
   localhost {
     reverse_proxy 127.0.0.1:8000
   }
   ```

3. **Run Django normally**:
   ```
   python manage.py runserver
   ```

4. **Run Caddy in another terminal**:
   ```
   caddy run
   ```

5. **Access your site at https://localhost**

## Option 2: Configure Django Settings for HTTPS

Even without running Django directly with HTTPS, you can configure it to use secure settings:

1. **Update settings.py**:
   - We've already added the necessary settings:
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

2. **Use environment variables**:
   - Create or update `.env` file with:
   ```
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

## Option 3: Use django-extensions with Werkzeug (For Unix-based systems)

This approach works better on Unix-based systems but can be challenging on Windows:

1. **Install required packages**:
   ```
   pip install django-extensions werkzeug pyOpenSSL
   ```

2. **Add to INSTALLED_APPS**:
   ```python
   INSTALLED_APPS = [
       # ...
       'django_extensions',
   ]
   ```

3. **Generate certificates**:
   ```
   python manage.py runserver_plus --cert-file ssl/server.crt --key-file ssl/server.key
   ```

## Production Considerations

For production environments, you should:

1. Use a proper SSL certificate from a trusted Certificate Authority
2. Configure your web server (Nginx, Apache) to handle HTTPS
3. Set up automatic certificate renewal with Let's Encrypt
4. Ensure all HTTPS security settings are enabled

By implementing any of these approaches, you'll satisfy the HTTPS requirement in Part 2 of the assignment, ensuring secure communication for your API during development.
