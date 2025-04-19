from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Course, Enrollment
from typing import Dict, Any, List

class UserDataExportSerializer(serializers.ModelSerializer):
    """Serializer for exporting all personal user data."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff']

# ... rest of the file remains unchanged ...
