"""
Unit tests for Green Academy API models.
These tests focus on testing model functionality in isolation.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Course, Module, Activity, Enrollment


class CourseModelTests(TestCase):
    """Test the Course model."""

    def setUp(self):
        """Set up test data."""
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )

    def test_course_creation(self):
        """Test creating a course."""
        course = Course.objects.create(
            title='Test Course',
            description='Course description',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.description, 'Course description')
        self.assertEqual(course.instructor, self.instructor)
        self.assertEqual(course.duration, '4 weeks')
        self.assertEqual(course.level, Course.LevelChoices.BEGINNER)
        self.assertTrue(course.is_featured)
    
    def test_course_string_representation(self):
        """Test the string representation of a course."""
        course = Course.objects.create(
            title='Test Course',
            description='Course description',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.assertEqual(str(course), 'Test Course')


class ModuleModelTests(TestCase):
    """Test the Module model."""

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

    def test_module_creation(self):
        """Test creating a module."""
        module = Module.objects.create(
            title='Test Module',
            description='Module description',
            course=self.course,
            order=1
        )
        
        self.assertEqual(module.title, 'Test Module')
        self.assertEqual(module.description, 'Module description')
        self.assertEqual(module.course, self.course)
        self.assertEqual(module.order, 1)
    
    def test_module_string_representation(self):
        """Test the string representation of a module."""
        module = Module.objects.create(
            title='Test Module',
            description='Module description',
            course=self.course,
            order=1
        )
        
        expected_str = f"{self.course.title} - {module.title}"
        self.assertEqual(str(module), expected_str)


class ActivityModelTests(TestCase):
    """Test the Activity model."""

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

    def test_activity_creation(self):
        """Test creating an activity."""
        activity = Activity.objects.create(
            title='Test Activity',
            description='Activity description',
            module=self.module,
            activity_type=Activity.TypeChoices.READING,
            order=1,
            content='Activity content'
        )
        
        self.assertEqual(activity.title, 'Test Activity')
        self.assertEqual(activity.description, 'Activity description')
        self.assertEqual(activity.module, self.module)
        self.assertEqual(activity.activity_type, Activity.TypeChoices.READING)
        self.assertEqual(activity.order, 1)
        self.assertEqual(activity.content, 'Activity content')
    
    def test_activity_string_representation(self):
        """Test the string representation of an activity."""
        activity = Activity.objects.create(
            title='Test Activity',
            description='Activity description',
            module=self.module,
            activity_type=Activity.TypeChoices.READING,
            order=1,
            content='Activity content'
        )
        
        self.assertEqual(str(activity), 'Test Activity')


class EnrollmentModelTests(TestCase):
    """Test the Enrollment model."""

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

    def test_enrollment_creation(self):
        """Test creating an enrollment."""
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            status=Enrollment.StatusChoices.ACTIVE,
            completion_percentage=50
        )
        
        self.assertEqual(enrollment.user, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.status, Enrollment.StatusChoices.ACTIVE)
        self.assertEqual(enrollment.completion_percentage, 50)
    
    def test_enrollment_string_representation(self):
        """Test the string representation of an enrollment."""
        enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            status=Enrollment.StatusChoices.ACTIVE,
            completion_percentage=50
        )
        
        expected_str = f"{self.student.username} - {self.course.title}"
        self.assertEqual(str(enrollment), expected_str)
