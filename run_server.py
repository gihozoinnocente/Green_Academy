import os
import sys
import time

# Force output to be unbuffered
os.environ['PYTHONUNBUFFERED'] = '1'

print("Starting Django server...")
print("Current directory:", os.getcwd())

# Run the Django development server
cmd = "python manage.py runserver 127.0.0.0:8000"
print(f"Running command: {cmd}")
sys.stdout.flush()  # Force output to display
exit_code = os.system(cmd)

print(f"Server process exited with code: {exit_code}")
