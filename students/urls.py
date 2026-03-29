from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('subject/<int:subject_id>/', views.subject_detail, name='student_subject_detail'),
    path('learn/<int:material_id>/', views.learn, name='student_learn'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='student_quiz'),
    path('quiz-result/<int:attempt_id>/', views.quiz_result, name='student_quiz_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('final-result/', views.final_result, name='final_result'),
]
