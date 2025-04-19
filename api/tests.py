from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from typing import Dict, Any, List, Optional, cast
from rest_framework.response import Response

from .models import Course, Enrollment


class CourseAPITestCase(TestCase):
    """Test case for the Course API."""
    
    def setUp(self) -> None:
        """Set up test data."""
        self.client = APIClient()
        
        # Create users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            title='Test Course 1',
            description='Course description 1',
            instructor=self.admin_user,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.course2 = Course.objects.create(
            title='Test Course 2',
            description='Course description 2',
            instructor=self.admin_user,
            duration='6 weeks',
            level=Course.LevelChoices.INTERMEDIATE,
            is_featured=False
        )
    
    def test_get_all_courses(self) -> None:
        """Test retrieving all courses."""
        url = reverse('course-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(getattr(response, 'data', {})['results']), 2)
    
    def test_get_course_detail(self) -> None:
        """Test retrieving a specific course."""
        course1_id = self.course1.id  # type: ignore[attr-defined]
        url = reverse('course-detail', kwargs={'pk': course1_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(getattr(response, 'data', {})['title'], 'Test Course 1')
    
    def test_create_course_as_admin(self) -> None:
        """Test creating a course as an admin user."""
        self.client.force_authenticate(user=self.admin_user)  # type: ignore[attr-defined]
        url = reverse('course-list')
        
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'instructor_id': self.admin_user.id,  # type: ignore
            'duration': '8 weeks',
            'level': Course.LevelChoices.ADVANCED,
            'is_featured': False
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 3)
    
    def test_create_course_as_regular_user(self) -> None:
        """Test that regular users cannot create courses."""
        self.client.force_authenticate(user=self.regular_user)  # type: ignore[attr-defined]
        url = reverse('course-list')
        
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'instructor_id': self.admin_user.id,  # type: ignore
            'duration': '8 weeks',
            'level': Course.LevelChoices.ADVANCED,
            'is_featured': False
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 2)


class EnrollmentAPITestCase(TestCase):
    """Test case for the Enrollment API."""
    
    def setUp(self) -> None:
        """Set up test data."""
        self.client = APIClient()
        
        # Create users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.student1 = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='student123'
        )
        
        self.student2 = User.objects.create_user(
            username='student2',
            email='student2@example.com',
            password='student123'
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            title='Test Course 1',
            description='Course description 1',
            instructor=self.admin_user,
            duration='4 weeks',
            level=Course.LevelChoices.BEGINNER,
            is_featured=True
        )
        
        self.course2 = Course.objects.create(
            title='Test Course 2',
            description='Course description 2',
            instructor=self.admin_user,
            duration='6 weeks',
            level=Course.LevelChoices.INTERMEDIATE,
            is_featured=False
        )
        
        # Create enrollments
        self.enrollment1 = Enrollment.objects.create(
            user=self.student1,
            course=self.course1,
            status=Enrollment.StatusChoices.ACTIVE,
            completion_percentage=25
        )
    
    def test_enroll_in_course(self) -> None:
        """Test enrolling a user in a course."""
        self.client.force_authenticate(user=self.student2)  # type: ignore[attr-defined]
        url = reverse('enrollment-list')
        
        student2_id = self.student2.id  # type: ignore[attr-defined]
        course1_id = self.course1.id  # type: ignore[attr-defined]
        data = {
            'user_id': student2_id,
            'course_id': course1_id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 2)
    
    def test_get_user_enrollments(self) -> None:
        """Test retrieving a user's enrollments."""
        self.client.force_authenticate(user=self.student1)  # type: ignore[attr-defined]
        student1_id = self.student1.id  # type: ignore[attr-defined]
        url = reverse('user-enrollments', kwargs={'user_id': student1_id})
        
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(getattr(response, 'data', {})['results']), 1)
        course1_id: int = self.course1.id  # type: ignore[attr-defined]
        self.assertEqual(getattr(response, 'data', {})['results'][0]['course']['id'], course1_id)
    
    def test_update_enrollment_status(self) -> None:
        """Test updating enrollment status."""
        self.client.force_authenticate(user=self.student1)  # type: ignore[attr-defined]
        url = reverse('enrollment-detail', kwargs={'pk': self.enrollment1.id})
        
        data = {
            'status': Enrollment.StatusChoices.COMPLETED,
            'completion_percentage': 100
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database
        self.enrollment1.refresh_from_db()
        self.assertEqual(self.enrollment1.status, Enrollment.StatusChoices.COMPLETED)
        self.assertEqual(self.enrollment1.completion_percentage, 100)