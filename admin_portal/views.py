import threading
import PyPDF2
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from students.models import Subject, Enrollment, LeaderboardEntry
from admin_portal.models import Material
from quiz.models import QuizAttempt, Quiz
from quiz.generator import generate_all_levels

User = get_user_model()

def dashboard(request):
    total_students = User.objects.filter(role='student').count()
    total_materials = Material.objects.count()
    quizzes_generated = Quiz.objects.count()
    active_this_week = LeaderboardEntry.objects.filter(weekly_points__gt=0).count()

    recent_attempts = QuizAttempt.objects.select_related('student', 'quiz__material').order_by('-attempted_at')[:10]

    context = {
        'total_students': total_students,
        'total_materials': total_materials,
        'quizzes_generated': quizzes_generated,
        'active_this_week': active_this_week,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'admin_portal/dashboard.html', context)

def materials_list(request):
    materials = Material.objects.select_related('subject', 'posted_by').order_by('-posted_at')
    return render(request, 'admin_portal/materials.html', {'materials': materials})

def extract_youtube_transcript(url):
    try:
        parsed_url = urlparse(url)
        video_id = ""
        if 'youtube.com' in parsed_url.netloc:
            query = parse_qs(parsed_url.query)
            video_id = query.get("v", [""])[0]
        elif 'youtu.be' in parsed_url.netloc:
            video_id = parsed_url.path.lstrip('/')
            
        if video_id:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([tr['text'] for tr in transcript_list])
    except Exception as e:
        return f"\n[Transcript unavailable: {str(e)}]\n"
    return ""

def material_new(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        level = request.POST.get('level')
        title = request.POST.get('title')
        material_type = request.POST.get('material_type', 'text')
        
        content = ""
        youtube_url = ""
        file_upload = None

        if material_type == 'text':
            content = request.POST.get('content', '')
        elif material_type == 'pdf':
            file_upload = request.FILES.get('file_upload')
            if file_upload and file_upload.name.endswith('.pdf'):
                reader = PyPDF2.PdfReader(file_upload)
                for page in reader.pages:
                    content += page.extract_text() or ""
        elif material_type == 'youtube':
            youtube_url = request.POST.get('youtube_url', '')
            if youtube_url:
                content = extract_youtube_transcript(youtube_url)

        subject = get_object_or_404(Subject, id=subject_id)
        material = Material.objects.create(
            subject=subject,
            level=level,
            title=title,
            content=content,
            youtube_url=youtube_url,
            file_upload=file_upload,
            posted_by=request.user
        )

        # Trigger background generator to not block UI
        def run_gen():
            generate_all_levels(material)
            
        t = threading.Thread(target=run_gen)
        t.start()

        messages.success(request, f"Material posted! Generating questions across all levels in the background.")
        return redirect('admin_materials')

    return render(request, 'admin_portal/material_new.html', {'subjects': subjects})

def students_list(request):
    students = User.objects.filter(role='student').prefetch_related('enrollments__subject')
    return render(request, 'admin_portal/students_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(User, id=student_id, role='student')
    enrollments = student.enrollments.select_related('subject')
    attempts = student.quiz_attempts.select_related('quiz__material').order_by('-attempted_at')
    
    return render(request, 'admin_portal/student_detail.html', {
        'student': student,
        'enrollments': enrollments,
        'attempts': attempts
    })

def leaderboard(request):
    entries = LeaderboardEntry.objects.select_related('student').order_by('-weekly_points')
    all_time = LeaderboardEntry.objects.select_related('student').order_by('-all_time_points')
    return render(request, 'admin_portal/leaderboard.html', {
        'weekly_entries': entries,
        'all_time_entries': all_time
    })
