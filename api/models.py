from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from typing import Any, Optional, List


class Course(models.Model):
    """Course model for Green Academy educational content."""
    
    class LevelChoices(models.TextChoices):
        BEGINNER = 'BEG', _('Beginner')
        INTERMEDIATE = 'INT', _('Intermediate')
        ADVANCED = 'ADV', _('Advanced')
    
    title: models.CharField = models.CharField(
        max_length=255,
        help_text=_("Title of the course")
    )
    description: models.TextField = models.TextField(
        help_text=_("Detailed description of the course")
    )
    instructor: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        help_text=_("User who teaches this course")
    )
    duration: models.CharField = models.CharField(
        max_length=50,
        help_text=_("Duration of the course (e.g., '6 weeks')")
    )
    level: models.CharField = models.CharField(
        max_length=3,
        choices=LevelChoices.choices,
        default=LevelChoices.BEGINNER,
        help_text=_("Difficulty level of the course")
    )
    is_featured: models.BooleanField = models.BooleanField(
        default=False,
        help_text=_("Whether this course is featured on the homepage")
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the course was created")
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text=_("When the course was last updated")
    )
    
    def __str__(self) -> str:
        return str(self.title)
    
    @property
    def enrollment_count(self) -> int:
        """Get the number of enrollments for this course."""
        enrollments = getattr(self, 'enrollments', None)
        if enrollments is not None:
            count: int = enrollments.count()
            return count
        return 0


class Enrollment(models.Model):
    """Enrollment model representing a user enrolled in a course."""
    
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACT', _('Active')
        COMPLETED = 'COM', _('Completed')
        PAUSED = 'PAU', _('Paused')
        DROPPED = 'DRO', _('Dropped')
    
    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text=_("User enrolled in the course")
    )
    course: models.ForeignKey = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        help_text=_("Course that the user is enrolled in")
    )
    enrolled_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the user enrolled in the course")
    )
    status: models.CharField = models.CharField(
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_("Current status of the enrollment")
    )
    completion_percentage: models.IntegerField = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Percentage of course completion (0-100)")
    )
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.course.title}"


class Module(models.Model):
    """Module model representing a section of a course."""
    
    course: models.ForeignKey = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        help_text=_("Course that this module belongs to")
    )
    title: models.CharField = models.CharField(
        max_length=255,
        help_text=_("Title of the module")
    )
    description: models.TextField = models.TextField(
        help_text=_("Detailed description of the module")
    )
    order: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text=_("Order of the module within the course")
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the module was created")
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text=_("When the module was last updated")
    )
    
    class Meta:
        ordering = ['course', 'order']
    
    def __str__(self) -> str:
        return f"{self.course.title} - {self.title}"
    
    @property
    def activity_count(self) -> int:
        """Get the number of activities in this module."""
        activities = getattr(self, 'activities', None)
        if activities is not None:
            count: int = activities.count()
            return count
        return 0


class Activity(models.Model):
    """Activity model representing a learning activity within a module."""
    
    class ActivityTypeChoices(models.TextChoices):
        LESSON = 'lesson', _('Lesson')
        QUIZ = 'quiz', _('Quiz')
        ASSIGNMENT = 'assignment', _('Assignment')
    
    module: models.ForeignKey = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text=_("Module that this activity belongs to")
    )
    title: models.CharField = models.CharField(
        max_length=255,
        help_text=_("Title of the activity")
    )
    description: models.TextField = models.TextField(
        help_text=_("Detailed description of the activity")
    )
    type: models.CharField = models.CharField(
        max_length=20,
        choices=ActivityTypeChoices.choices,
        default=ActivityTypeChoices.LESSON,
        help_text=_("Type of activity")
    )
    content: models.TextField = models.TextField(
        blank=True,
        help_text=_("Content of the activity (e.g., lesson text, quiz questions)")
    )
    order: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text=_("Order of the activity within the module")
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When the activity was created")
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        help_text=_("When the activity was last updated")
    )
    
    class Meta:
        ordering = ['module', 'order']
        verbose_name_plural = 'activities'
    
    def __str__(self) -> str:
        return f"{self.module.title} - {self.title}"