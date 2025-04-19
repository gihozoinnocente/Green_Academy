import sys
import django

print("Python version:", sys.version)
print("Django version:", django.get_version())
print("This is a test of console output")

# Try a minimal django server start
if __name__ == '__main__':
    print("Starting test...")
    from django.core.management import execute_from_command_line
    print("Imported execute_from_command_line")
    execute_from_command_line(['test_server.py', 'runserver', '--noreload'])
