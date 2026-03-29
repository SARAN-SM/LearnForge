from django.db import models
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    LEVEL_CHOICES = (
        ('BEGINNER', 'BEGINNER'),
        ('INTERMEDIATE', 'INTERMEDIATE'),
        ('ADVANCED', 'ADVANCED'),
    )
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'IN PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    initial_marks = models.IntegerField(default=0)
    starting_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    subject_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    
    beginner_done = models.BooleanField(default=False)
    intermediate_done = models.BooleanField(default=False)
    advanced_done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} ({self.current_level})"

class LeaderboardEntry(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaderboard')
    weekly_points = models.IntegerField(default=0)
    all_time_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_active = models.DateField(auto_now_add=True)
    week_reset_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.all_time_points} pts"
