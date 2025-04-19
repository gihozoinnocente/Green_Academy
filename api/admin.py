from django.contrib import admin
from .models import Course, Enrollment
from typing import List, Tuple, Any, Optional


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'level', 'duration', 'is_featured', 'created_at')
    list_filter = ('level', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    date_hierarchy = 'created_at'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'completion_percentage', 'enrolled_at')
    list_filter = ('status', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'enrolled_at'