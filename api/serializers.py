from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Course, Enrollment, Module, Activity
from typing import Dict, Any, List


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Add 'is_staff' as a writable field for instructor/admin creation.
    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.groups.filter(name="instructors").exists():
            data['role'] = 'instructor'
        elif instance.is_staff:
            data['role'] = 'admin'
        elif instance.groups.filter(name="students").exists():
            data['role'] = 'student'
        else:
            data['role'] = 'student'  # fallback
        return data

    is_staff = serializers.BooleanField(required=False, help_text="Designates whether the user can access the admin site and is considered an instructor/admin.")
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    role = serializers.ChoiceField(
        choices=[("student", "student"), ("instructor", "instructor"), ("admin", "admin")],
        required=False,
        default="admin"
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'password', 'date_joined', 'is_active', 'is_staff', 'role']
        read_only_fields = ['id', 'date_joined', 'is_active']
        
    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create and return a new user with encrypted password, with robust error handling and role assignment. Accepts is_staff as an API field."""
        from django.db import IntegrityError
        from rest_framework import serializers
        from django.contrib.auth.models import Group

        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email', '')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        role = validated_data.get('role', None)
        is_staff = validated_data.get('is_staff', False)

        # Validate required fields
        if not username:
            raise serializers.ValidationError({'username': 'This field is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'This field is required.'})

        # Check uniqueness
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'A user with that username already exists.'})
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'A user with that email already exists.'})

        # Validate password
        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        # Validate and assign role
        valid_roles = ["student", "instructor", "admin"]
        if role and role not in valid_roles:
            raise serializers.ValidationError({'role': f"Role must be one of {valid_roles}"})

        try:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff or (role == "admin" or role == "instructor")
            )
            user.set_password(password)
            user.save()
            if role:
                if role == "admin":
                    group, _ = Group.objects.get_or_create(name="admins")
                    user.groups.add(group)
                elif role == "instructor":
                    group, _ = Group.objects.get_or_create(name="instructors")
                    user.groups.add(group)
                elif role == "student":
                    group, _ = Group.objects.get_or_create(name="students")
                    user.groups.add(group)
        except IntegrityError as e:
            raise serializers.ValidationError({'detail': 'Failed to create user due to a database error.'})
        return user


class UserLimitedSerializer(serializers.ModelSerializer):
    """Simplified User serializer for nested representations."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class InstructorSerializer(serializers.ModelSerializer):
    """Serializer for instructor representation in courses."""
    
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name']
        
    def get_name(self, obj: User) -> str:
        """Get the full name of the instructor."""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for Course model when listing courses."""
    
    instructor = InstructorSerializer(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'duration', 
                  'level', 'is_featured', 'created_at', 'updated_at', 
                  'enrollment_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'enrollment_count']


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Course instances."""
    
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True),
        source='instructor'
    )
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor_id', 'duration', 
                  'level', 'is_featured']
        read_only_fields = ['id']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer for Course model when retrieving a single course."""
    
    instructor = InstructorSerializer(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'duration', 
                  'level', 'is_featured', 'created_at', 'updated_at', 
                  'enrollment_count']
        read_only_fields = fields


class EnrollmentListSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model when listing enrollments."""
    
    user = UserLimitedSerializer(read_only=True)
    course = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at', 'status', 
                  'completion_percentage']
        read_only_fields = fields
        
    def get_course(self, obj: Enrollment) -> Dict[str, Any]:
        """Get a simplified representation of the course."""
        return {
            'id': obj.course.id,
            'title': obj.course.title
        }


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Enrollment instances."""
    
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course'
    )
    
    class Meta:
        model = Enrollment
        fields = ['user_id', 'course_id']
        
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that the user is not already enrolled in the course."""
        user = data.get('user')
        course = data.get('course')
        
        if Enrollment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError(
                {"detail": "User is already enrolled in this course."}
            )
            
        return data


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Enrollment instances."""
    
    class Meta:
        model = Enrollment
        fields = ['status', 'completion_percentage']


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single enrollment."""
    
    user = UserLimitedSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at', 'status', 
                  'completion_percentage']
        read_only_fields = fields


class ModuleListSerializer(serializers.ModelSerializer):
    """Serializer for Module model when listing modules."""
    
    activity_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'course_id', 'title', 'description', 'order',
                  'created_at', 'updated_at', 'activity_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'activity_count']


class ModuleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Module instances."""
    
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course'
    )
    
    class Meta:
        model = Module
        fields = ['id', 'course_id', 'title', 'description', 'order']
        read_only_fields = ['id']


class ModuleDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single module with activities."""
    
    activity_count = serializers.IntegerField(read_only=True)
    course = CourseListSerializer(read_only=True)
    activities = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order',
                  'created_at', 'updated_at', 'activity_count', 'activities']
        read_only_fields = fields
        
    def get_activities(self, obj) -> List[Dict[str, Any]]:
        """Get activities for this module."""
        activities = obj.activities.all().order_by('order')
        return ActivityListSerializer(activities, many=True).data


class ActivityListSerializer(serializers.ModelSerializer):
    """Serializer for Activity model when listing activities."""
    
    class Meta:
        model = Activity
        fields = ['id', 'module_id', 'title', 'description', 'type', 'order',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Activity instances."""
    
    module_id = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        source='module'
    )
    
    class Meta:
        model = Activity
        fields = ['id', 'module_id', 'title', 'description', 'type', 'content', 'order']
        read_only_fields = ['id']


class ActivityDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single activity."""
    
    module = ModuleListSerializer(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'module', 'title', 'description', 'type', 'content', 'order',
                  'created_at', 'updated_at']
        read_only_fields = fields