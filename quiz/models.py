from django.db import models
from django.conf import settings
from admin_portal.models import Material

class Quiz(models.Model):
    LEVEL_CHOICES = (
        ('BEGINNER', 'BEGINNER'),
        ('INTERMEDIATE', 'INTERMEDIATE'),
        ('ADVANCED', 'ADVANCED'),
    )

    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='quizzes')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.material.title} ({self.level})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_index = models.IntegerField() # 0 for A, 1 for B, 2 for C, 3 for D
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Q: {self.question_text[:50]}..."

class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0) # 0 to 100
    passed = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.material.title} - Score: {self.score}"
