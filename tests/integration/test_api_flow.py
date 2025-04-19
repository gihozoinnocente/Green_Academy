"""
Integration tests for the Green Academy API workflow.
These tests focus on how different API endpoints work together in common user flows.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Course, Enrollment, Module, Activity


class StudentLearningFlowTests(TestCase):
    """Test the complete student learning flow through the API."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create users
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
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
        
        # Authenticate as admin initially
        self.client.force_authenticate(user=self.admin)
        
        # Create a course
        self.course = Course.objects.create(
            title='Integration Test Course',
            description='Course for integration testing',
            instructor=self.instructor,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        # Create modules
        self.module1 = Module.objects.create(
            title='Module 1',
            description='First module',
            course=self.course,
            order=1
        )
        
        self.module2 = Module.objects.create(
            title='Module 2',
            description='Second module',
            course=self.course,
            order=2
        )
        
        # Create activities
        Activity.objects.create(
            title='Activity 1.1',
            description='First activity of first module',
            module=self.module1,
            activity_type=Activity.TypeChoices.READING,
            order=1,
            content='Reading content for activity 1.1'
        )
        
        Activity.objects.create(
            title='Activity 1.2',
            description='Second activity of first module',
            module=self.module1,
            activity_type=Activity.TypeChoices.VIDEO,
            order=2,
            content='Video URL for activity 1.2'
        )
        
        Activity.objects.create(
            title='Activity 2.1',
            description='First activity of second module',
            module=self.module2,
            activity_type=Activity.TypeChoices.QUIZ,
            order=1,
            content='Quiz content for activity 2.1'
        )

    def test_complete_student_learning_journey(self):
        """Test a complete student learning journey from browsing to completion."""
        # Step 1: Student browses available courses
        self.client.force_authenticate(user=self.student)
        
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 1)
        else:
            self.assertEqual(len(response.data), 1)
        
        # Step 2: Student views course details
        url = reverse('course-detail', kwargs={'pk': self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        if isinstance(response.data, dict):
            self.assertEqual(response.data['title'], 'Integration Test Course')
        
        # Step 3: Student enrolls in the course
        url = reverse('enrollment-list')
        enrollment_data = {
            'user_id': self.student.id,
            'course_id': self.course.id
        }
        
        response = self.client.post(url, enrollment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        enrollment_id = response.data['id']
        
        # Step 4: Student views course modules
        url = reverse('course-modules', kwargs={'course_id': self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 2)  # Should see both modules
            modules_data = response.data['results']
        else:
            self.assertEqual(len(response.data), 2)  # Should see both modules
            modules_data = response.data
        
        # Step 5: Student views module activities
        url = reverse('module-activities', kwargs={'module_id': self.module1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 2)  # Should see both activities in module 1
            activities_data = response.data['results']
        else:
            self.assertEqual(len(response.data), 2)  # Should see both activities in module 1
            activities_data = response.data
        
        # Step 6: Student completes activities and updates progress
        url = reverse('enrollment-detail', kwargs={'pk': enrollment_id})
        update_data = {
            'completion_percentage': 50
        }
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        if isinstance(response.data, dict):
            self.assertEqual(response.data['completion_percentage'], 50)
        
        # Step 7: Student marks course as completed
        update_data = {
            'completion_percentage': 100,
            'status': Enrollment.StatusChoices.COMPLETED
        }
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        if isinstance(response.data, dict):
            self.assertEqual(response.data['completion_percentage'], 100)
            self.assertEqual(response.data['status'], Enrollment.StatusChoices.COMPLETED)
        
        # Step 8: Student views their enrollments
        url = reverse('user-enrollments', kwargs={'user_id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 1)
            enrollments_data = response.data['results']
        else:
            self.assertEqual(len(response.data), 1)
            enrollments_data = response.data
        
        # Check the enrollment data
        if 'course_title' in enrollments_data[0]:
            self.assertEqual(enrollments_data[0]['course_title'], 'Integration Test Course')
            self.assertEqual(enrollments_data[0]['completion_percentage'], 100)
        elif 'course' in enrollments_data[0] and isinstance(enrollments_data[0]['course'], dict):
            self.assertEqual(enrollments_data[0]['course']['title'], 'Integration Test Course')
            self.assertEqual(enrollments_data[0]['completion_percentage'], 100)


class InstructorCourseManagementTests(TestCase):
    """Test the instructor course management flow through the API."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create users
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='instructor123'
        )
        
        # Authenticate as instructor
        self.client.force_authenticate(user=self.instructor)

    def test_complete_course_creation_and_management(self):
        """Test a complete instructor flow for creating and managing a course."""
        # Step 1: Instructor attempts to create a new course but is forbidden
        # (based on current API implementation, only admins can create courses)
        url = reverse('course-list')
        course_data = {
            'title': 'New Instructor Course',
            'description': 'Course created by instructor',
            'instructor_id': self.instructor.id,
            'duration': '8 weeks',
            'level': Course.LevelChoices.INTERMEDIATE,
            'is_featured': False
        }
        
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Since instructors can't create courses, we'll create one as admin for testing
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Switch back to instructor for the rest of the test
        self.client.force_authenticate(user=self.instructor)
        
        # Check response structure
        if isinstance(response.data, dict) and 'id' in response.data:
            course_id = response.data['id']
        else:
            self.fail("Failed to get course_id from response")
        
        # Step 2: Instructor adds modules to the course
        url = reverse('module-list')
        module1_data = {
            'title': 'Introduction Module',
            'description': 'Introduction to the course',
            'course_id': course_id,
            'order': 1
        }
        
        response = self.client.post(url, module1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response structure
        if isinstance(response.data, dict) and 'id' in response.data:
            module1_id = response.data['id']
        else:
            self.fail("Failed to get module1_id from response")
        
        module2_data = {
            'title': 'Advanced Module',
            'description': 'Advanced topics',
            'course_id': course_id,
            'order': 2
        }
        
        response = self.client.post(url, module2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response structure
        if isinstance(response.data, dict) and 'id' in response.data:
            module2_id = response.data['id']
        else:
            self.fail("Failed to get module2_id from response")
        
        # Step 3: Instructor adds activities to modules
        url = reverse('activity-list')
        activity1_data = {
            'title': 'Introduction Reading',
            'description': 'Introduction reading material',
            'module_id': module1_id,
            'activity_type': Activity.TypeChoices.READING,
            'order': 1,
            'content': 'Reading content for introduction'
        }
        
        response = self.client.post(url, activity1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        activity2_data = {
            'title': 'Advanced Exercise',
            'description': 'Advanced practical exercise',
            'module_id': module2_id,
            'activity_type': Activity.TypeChoices.ASSIGNMENT,
            'order': 1,
            'content': 'Assignment instructions for advanced exercise'
        }
        
        response = self.client.post(url, activity2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Step 4: Instructor updates course details
        url = reverse('course-detail', kwargs={'pk': course_id})
        update_data = {
            'title': 'Updated Course Title',
            'is_featured': True
        }
        
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        if isinstance(response.data, dict):
            self.assertEqual(response.data['title'], 'Updated Course Title')
            self.assertTrue(response.data['is_featured'])
        
        # Step 5: Instructor views course modules
        url = reverse('course-modules', kwargs={'course_id': course_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 2)
            modules_data = response.data['results']
        else:
            self.assertEqual(len(response.data), 2)
            modules_data = response.data
        
        # Step 6: Instructor views module activities
        url = reverse('module-activities', kwargs={'module_id': module1_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 1)
            self.assertEqual(response.data['results'][0]['title'], 'Introduction Reading')
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], 'Introduction Reading')
        
        # Step 7: Instructor views course enrollments (should be empty initially)
        url = reverse('course-enrollments', kwargs={'course_id': course_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertEqual(response.data['count'], 0)
        else:
            self.assertEqual(len(response.data), 0)
