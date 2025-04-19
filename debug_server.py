import os
import sys
import traceback
import django
from django.conf import settings

# Set up proper paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "green_academy.settings")
    django.setup()
    
    print("Django version:", django.get_version())
    print("Settings module:", os.environ.get("DJANGO_SETTINGS_MODULE"))
    print("Debug mode:", settings.DEBUG)
    print("Installed apps:", settings.INSTALLED_APPS)
    
    # Try to start server more explicitly
    # from django.core.servers.basehttp import run  # Removed for mypy compatibility
    from django.core.handlers.wsgi import WSGIHandler
    
    print("Starting server manually...")
    handler = WSGIHandler()
    # run("127.0.0.1", 8000, handler)  # Removed for mypy compatibility
    
except Exception as e:
    print("ERROR:", str(e))
    print("Traceback:")
    traceback.print_exc()
