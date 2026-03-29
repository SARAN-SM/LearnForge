from django.db import models
from django.conf import settings
from students.models import Subject

class Material(models.Model):
    LEVEL_CHOICES = (
        ('BEGINNER', 'BEGINNER'),
        ('INTERMEDIATE', 'INTERMEDIATE'),
        ('ADVANCED', 'ADVANCED'),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    content = models.TextField() # Markdown content
    file_upload = models.FileField(upload_to='materials/', null=True, blank=True)
    youtube_url = models.URLField(max_length=500, null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject.name} - {self.level})"
