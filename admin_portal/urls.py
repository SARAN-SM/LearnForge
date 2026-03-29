from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('materials/', views.materials_list, name='admin_materials'),
    path('materials/new/', views.material_new, name='admin_material_new'),
    path('students/', views.students_list, name='admin_students'),
    path('students/<int:student_id>/', views.student_detail, name='admin_student_detail'),
    path('leaderboard/', views.leaderboard, name='admin_leaderboard'),
]
