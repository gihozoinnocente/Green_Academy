"""
Unit tests for Green Academy API serializers.
These tests focus on testing serializer functionality in isolation.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from api.models import Course, Module, Activity, Enrollment
from api.serializers import (
    UserSerializer, CourseListSerializer, CourseDetailSerializer, CourseCreateUpdateSerializer,
    ModuleListSerializer, ModuleCreateSerializer, ModuleDetailSerializer,
    ActivityListSerializer, ActivityCreateSerializer, ActivityDetailSerializer,
    EnrollmentListSerializer, EnrollmentCreateSerializer, EnrollmentDetailSerializer
)


class UserSerializerTests(TestCase):
    """Test the UserSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user_attributes = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.user = User.objects.create_user(**self.user_attributes)
        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'role']
        )
    
    def test_field_content(self):
        """Test that the serializer fields contain the correct data."""
        data = self.serializer.data
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
    
    def test_password_write_only(self):
        """Test that the password field is write-only."""
        data = self.serializer.data
        self.assertNotIn('password', data)


class CourseSerializerTests(TestCase):
    """Test the CourseSerializer."""

    def setUp(self):
        """Set up test data."""
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )
        
        self.course_attributes = {
            'title': 'Test Course',
            'description': 'Course description',
            'instructor': self.instructor,
            'duration': '4 weeks',
            'level': Course.LevelChoices.BEGINNER,
            'is_featured': True
        }
        
        self.course = Course.objects.create(**self.course_attributes)
        self.serializer = CourseListSerializer(instance=self.course)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'title', 'description', 'instructor', 'duration', 
             'level', 'is_featured', 'created_at', 'updated_at', 'enrollment_count']
        )
    
    def test_field_content(self):
        """Test that the serializer fields contain the correct data."""
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Course')
        self.assertEqual(data['description'], 'Course description')
        self.assertEqual(data['instructor']['id'], self.instructor.id)
        self.assertEqual(data['duration'], '4 weeks')
        self.assertEqual(data['level'], Course.LevelChoices.BEGINNER)
        self.assertTrue(data['is_featured'])


class ModuleSerializerTests(TestCase):
    """Test the ModuleSerializer."""

    def setUp(self):
        """Set up test data."""
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course description',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.module_attributes = {
            'title': 'Test Module',
            'description': 'Module description',
            'course': self.course,
            'order': 1
        }
        
        self.module = Module.objects.create(**self.module_attributes)
        self.serializer = ModuleListSerializer(instance=self.module)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'course_id', 'title', 'description', 'order', 'created_at', 'updated_at', 'activity_count']
        )
    
    def test_field_content(self):
        """Test that the serializer fields contain the correct data."""
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Module')
        self.assertEqual(data['description'], 'Module description')
        self.assertEqual(data['course_id'], self.course.id)
        self.assertEqual(data['order'], 1)


class ActivitySerializerTests(TestCase):
    """Test the ActivitySerializer."""

    def setUp(self):
        """Set up test data."""
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course description',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.module = Module.objects.create(
            title='Test Module',
            description='Module description',
            course=self.course,
            order=1
        )
        
        self.activity_attributes = {
            'title': 'Test Activity',
            'description': 'Activity description',
            'module': self.module,
            'activity_type': Activity.TypeChoices.READING,
            'order': 1,
            'content': 'Activity content'
        }
        
        self.activity = Activity.objects.create(**self.activity_attributes)
        self.serializer = ActivityListSerializer(instance=self.activity)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'module_id', 'title', 'description', 'type', 
             'order', 'created_at', 'updated_at']
        )
    
    def test_field_content(self):
        """Test that the serializer fields contain the correct data."""
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Activity')
        self.assertEqual(data['description'], 'Activity description')
        self.assertEqual(data['module_id'], self.module.id)
        self.assertEqual(data['type'], Activity.TypeChoices.READING)
        self.assertEqual(data['order'], 1)


class EnrollmentSerializerTests(TestCase):
    """Test the EnrollmentSerializer."""

    def setUp(self):
        """Set up test data."""
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )
        
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='student123'
        )
        
        self.course = Course.objects.create(
            title='Test Course',
            description='Course description',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.enrollment_attributes = {
            'user': self.student,
            'course': self.course,
            'status': Enrollment.StatusChoices.ACTIVE,
            'completion_percentage': 50
        }
        
        self.enrollment = Enrollment.objects.create(**self.enrollment_attributes)
        self.serializer = EnrollmentListSerializer(instance=self.enrollment)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'user', 'course', 'enrolled_at', 'status', 'completion_percentage']
        )
    
    def test_field_content(self):
        """Test that the serializer fields contain the correct data."""
        data = self.serializer.data
        self.assertEqual(data['user']['id'], self.student.id)
        self.assertEqual(data['course']['id'], self.course.id)
        self.assertEqual(data['status'], Enrollment.StatusChoices.ACTIVE)
        self.assertEqual(data['completion_percentage'], 50)
