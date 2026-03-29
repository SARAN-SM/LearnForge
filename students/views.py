import markdown
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Enrollment, Subject, LeaderboardEntry
from admin_portal.models import Material
from quiz.models import Quiz, Question, QuizAttempt
from quiz.generator import generate_quiz_for_material

def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('subject')
    entry, _ = LeaderboardEntry.objects.get_or_create(student=request.user)
    
    return render(request, 'students/dashboard.html', {
        'enrollments': enrollments,
        'points': entry.all_time_points
    })

def subject_detail(request, subject_id):
    enrollment = get_object_or_404(Enrollment, student=request.user, subject_id=subject_id)
    materials = Material.objects.filter(subject_id=subject_id).order_by('level')
    
    return render(request, 'students/subject_detail.html', {
        'enrollment': enrollment,
        'materials': materials
    })

def learn(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    html_content = markdown.markdown(material.content)
    
    # Check if quiz exists for this level
    quiz = Quiz.objects.filter(material=material, level=material.level).first()
    
    return render(request, 'students/learn.html', {
        'material': material,
        'html_content': html_content,
        'quiz': quiz
    })

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, subject=quiz.material.subject)
    
    # Check if they belong to this level
    if quiz.level != enrollment.current_level and enrollment.subject_status != 'COMPLETED':
        pass # Optional: restrictive check. Allowed for retry

    if request.method == 'GET':
        # User requested: "generate different questions on each referesh page and each test"
        generate_quiz_for_material(quiz.material, quiz.level)
        quiz.refresh_from_db()
        
    questions = quiz.questions.all()

    if request.method == 'POST':
        score_val = 0
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected is not None and int(selected) == q.correct_index:
                score_val += 1
                
        final_score = int((score_val / len(questions)) * 100) if len(questions) > 0 else 0
        
        # Determine promotion
        passed = False
        promoted = False
        completed = False
        
        if quiz.level == 'BEGINNER' and final_score >= 70:
            passed = True
            if not enrollment.beginner_done:
                enrollment.beginner_done = True
                enrollment.current_level = 'INTERMEDIATE'
                promoted = True
        elif quiz.level == 'INTERMEDIATE' and final_score >= 75:
            passed = True
            if not enrollment.intermediate_done:
                enrollment.intermediate_done = True
                enrollment.current_level = 'ADVANCED'
                promoted = True
        elif quiz.level == 'ADVANCED' and final_score >= 80:
            passed = True
            if not enrollment.advanced_done:
                enrollment.advanced_done = True
                enrollment.subject_status = 'COMPLETED'
                completed = True
        
        enrollment.save()
        
        # Calculate points
        multiplier = 1.0
        if quiz.level == 'INTERMEDIATE': multiplier = 1.5
        elif quiz.level == 'ADVANCED': multiplier = 2.0
        
        base_points = final_score
        level_points = int(base_points * multiplier)
        
        bonus = 0
        if promoted: bonus += 50
        if completed: bonus += 100
        
        entry = request.user.leaderboard
        
        # Streak logic
        today = date.today()
        if entry.last_active == today - timedelta(days=1):
            entry.streak_days += 1
            bonus += 20
        elif entry.last_active < today - timedelta(days=1):
            entry.streak_days = 1 # Reset if missed
        else:
            pass # Same day, streak persists, no extra bonus

        entry.last_active = today
        
        total_points = level_points + bonus
        entry.weekly_points += total_points
        entry.all_time_points += total_points
        entry.save()
        
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=final_score,
            passed=passed,
            points_earned=total_points
        )
        
        # if failed, generate a fresh new quiz behind the scenes
        if not passed:
            generate_quiz_for_material(quiz.material, quiz.level)
            
        return redirect('student_quiz_result', attempt_id=attempt.id)
        
    return render(request, 'students/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    # Need to deduce points breakdown. 
    multiplier = 1.0
    if attempt.quiz.level == 'INTERMEDIATE': multiplier = 1.5
    elif attempt.quiz.level == 'ADVANCED': multiplier = 2.0
    
    level_points = int(attempt.score * multiplier)
    
    # Rough estimate of bonuses
    diff = attempt.points_earned - level_points
    promoted = diff >= 50 and diff < 100 or diff >= 70
    completed = diff >= 100
    streak_bonus = diff % 50 if diff > 0 else 0
    
    return render(request, 'students/quiz_result.html', {
        'attempt': attempt,
        'multiplier': multiplier,
        'level_points': level_points,
        'promoted': promoted,
        'completed': completed,
        'streak_bonus': streak_bonus,
    })

def reset_weekly_if_needed(entry):
    now = timezone.now()
    monday = now - timedelta(days=now.weekday())
    monday_midnight = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if entry.week_reset_at < monday_midnight:
        entry.weekly_points = 0
        entry.week_reset_at = now
        entry.save()

def leaderboard(request):
    entry, _ = LeaderboardEntry.objects.get_or_create(student=request.user)
    reset_weekly_if_needed(entry)
    
    entries = LeaderboardEntry.objects.select_related('student').order_by('-weekly_points')
    # Loop and reset all others just in case
    for e in entries:
        reset_weekly_if_needed(e)
        
    weekly = LeaderboardEntry.objects.select_related('student').order_by('-weekly_points')
    all_time = LeaderboardEntry.objects.select_related('student').order_by('-all_time_points')
    
    return render(request, 'students/leaderboard.html', {
        'weekly_entries': weekly,
        'all_time_entries': all_time
    })

def final_result(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    if not enrollments.exists():
        messages.warning(request, "Enroll in subjects first.")
        return redirect('student_dashboard')
        
    for e in enrollments:
        if e.subject_status != 'COMPLETED':
            messages.warning(request, "You must complete ALL enrolled subjects to view the final certificate.")
            return redirect('student_dashboard')
            
    entry = request.user.leaderboard
    return render(request, 'students/final_result.html', {
        'enrollments': enrollments,
        'entry': entry
    })
