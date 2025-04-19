"""
Performance tests for load handling in the Green Academy API.
These tests focus on measuring the API's performance under load.
"""
import time
import threading
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Course, Enrollment


class ConcurrentRequestsPerformanceTest(TransactionTestCase):
    """Test the API's performance under concurrent requests."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Create multiple courses (30)
        for i in range(30):
            Course.objects.create(
                title=f'Test Course {i}',
                description=f'Course description {i}',
                instructor=self.admin_user,
                duration='4 weeks',
                level=Course.LevelChoices.BEGINNER,
                is_featured=(i % 3 == 0)  # Every third course is featured
            )
    
    def test_concurrent_course_requests(self):
        """Test the API's performance with concurrent course list requests."""
        url = reverse('course-list')
        
        # Establish baseline with a single request
        start_time = time.time()
        response = self.client.get(url)
        baseline_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with concurrent requests
        num_threads = 10
        request_times = []
        
        def make_request():
            """Make a request and record the time it takes."""
            client = APIClient()
            start_time = time.time()
            response = client.get(url)
            request_time = time.time() - start_time
            
            # Store the request time
            request_times.append(request_time)
            
            # Verify the response is correct
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Check if response is paginated
            if isinstance(response.data, dict) and 'results' in response.data:
                # Check that we're getting paginated results (default is 10 items per page)
                self.assertEqual(response.data['count'], 30)  # Total count should be 30
                self.assertLessEqual(len(response.data['results']), 10)  # Default page size
            else:
                # If not paginated, we should get all items
                self.assertEqual(len(response.data), 30)
        
        # Create and start threads
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Calculate average request time
        avg_concurrent_time = sum(request_times) / len(request_times)
        
        # Print performance metrics
        print(f"Baseline request time: {baseline_time:.4f}s")
        print(f"Average concurrent request time: {avg_concurrent_time:.4f}s")
        
        # The average concurrent time should not be significantly higher than the baseline
        # Allow for some degradation but not more than 3x
        # Only compare if baseline_time is not zero
        if baseline_time > 0:
            self.assertLess(avg_concurrent_time, baseline_time * 3)
        else:
            # If baseline_time is zero, just make sure avg_concurrent_time is reasonable
            self.assertLess(avg_concurrent_time, 1.0)  # Less than 1 second is reasonable
    
    def test_concurrent_write_operations(self):
        """Test the API's performance with concurrent write operations."""
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Create multiple students
        students = []
        for i in range(10):
            student = User.objects.create_user(
                username=f'student{i}',
                email=f'student{i}@example.com',
                password='student123'
            )
            students.append(student)
        
        # Get a course ID
        course = Course.objects.first()
        
        # Test with concurrent enrollment creations
        num_threads = 10
        success_count = [0]  # Using a list to allow modification in nested function
        
        def create_enrollment(student_index):
            """Create an enrollment for a student."""
            client = APIClient()
            client.force_authenticate(user=self.admin_user)
            
            url = reverse('enrollment-list')
            enrollment_data = {
                'user_id': students[student_index].id,
                'course_id': course.id
            }
            
            response = client.post(url, enrollment_data, format='json')
            if response.status_code == status.HTTP_201_CREATED:
                success_count[0] += 1
        
        # Create and start threads
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=create_enrollment, args=(i,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Print performance metrics
        print(f"Concurrent enrollment creations attempted: {num_threads}")
        print(f"Successful enrollment creations: {success_count[0]}")
        
        # All enrollments should be created successfully
        self.assertEqual(success_count[0], num_threads)
        
        # Verify in the database
        try:
            enrollment_count = Enrollment.objects.filter(course=course).count()
            self.assertEqual(enrollment_count, num_threads)
        except Exception as e:
            self.fail(f"Database verification failed: {str(e)}")


class PaginationPerformanceTests(TestCase):
    """Test the performance of pagination."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Create multiple courses (100)
        for i in range(100):
            Course.objects.create(
                title=f'Test Course {i}',
                description=f'Course description {i}',
                instructor=self.admin_user,
                duration='4 weeks',
                level=Course.LevelChoices.BEGINNER,
                is_featured=(i % 3 == 0)  # Every third course is featured
            )
    
    def test_pagination_performance(self):
        """Test that pagination improves performance for large datasets."""
        # Test without pagination (if possible)
        url = reverse('course-list')
        params = {'limit': 100}  # Try to get all courses
        
        start_time = time.time()
        response = self.client.get(url, params)
        full_request_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with pagination
        params = {'limit': 10, 'offset': 0}
        
        start_time = time.time()
        response = self.client.get(url, params)
        paginated_request_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Only compare times if both requests were successful and returned different result sets
        if paginated_request_time > 0 and full_request_time > 0:
            # The paginated request should be faster
            self.assertLess(paginated_request_time, full_request_time)
        
        # Print performance metrics
        print(f"Full request time: {full_request_time:.4f}s")
        print(f"Paginated request time: {paginated_request_time:.4f}s")
        print(f"Performance improvement: {(1 - paginated_request_time/full_request_time) * 100:.2f}%")
        
        # Verify pagination works correctly
        if isinstance(response.data, dict) and 'results' in response.data:
            self.assertLessEqual(len(response.data['results']), 10)
            self.assertTrue('count' in response.data or 'next' in response.data)
        else:
            # If not paginated, we should still have a reasonable response
            self.assertLessEqual(len(response.data), 100)
    
    def test_pagination_navigation(self):
        """Test the performance of navigating through paginated results."""
        url = reverse('course-list')
        
        # First page
        params = {'limit': 10, 'offset': 0}
        
        start_time = time.time()
        response = self.client.get(url, params)
        first_page_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Second page
        params = {'limit': 10, 'offset': 10}
        
        start_time = time.time()
        response = self.client.get(url, params)
        second_page_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Last page
        params = {'limit': 10, 'offset': 90}
        
        start_time = time.time()
        response = self.client.get(url, params)
        last_page_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Print performance metrics
        print(f"First page request time: {first_page_time:.4f}s")
        print(f"Second page request time: {second_page_time:.4f}s")
        print(f"Last page request time: {last_page_time:.4f}s")
        
        # All page requests should be reasonably fast
        self.assertLess(first_page_time, 0.5)  # Less than 500ms
        self.assertLess(second_page_time, 0.5)
        self.assertLess(last_page_time, 0.5)
