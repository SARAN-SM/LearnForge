from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from students.models import Subject, Enrollment, LeaderboardEntry

User = get_user_model()

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and getattr(user, 'role', '') == 'student':
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid student credentials.')
    return render(request, 'accounts/student_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and getattr(user, 'role', '') == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'accounts/admin_login.html')

def student_signup(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        # Registration fields
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('student_signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('student_signup')

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists.")
            return redirect('student_signup')

        # Create student user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.role = 'student'
        user.save()

        # Initialize leaderboard entry
        LeaderboardEntry.objects.create(student=user)

        # Process chosen subjects
        selected_subjects = request.POST.getlist('subjects')
        for subject_id in selected_subjects:
            marks_str = request.POST.get(f'marks_{subject_id}', '0')
            try:
                marks = int(marks_str)
            except ValueError:
                marks = 0
            
            # Determine level
            starting_level = 'BEGINNER'
            b_done, i_done, a_done = False, False, False
            if marks >= 70:
                starting_level = 'ADVANCED'
                b_done, i_done = True, True
            elif marks >= 40:
                starting_level = 'INTERMEDIATE'
                b_done = True
                
            subject_obj = Subject.objects.get(id=subject_id)
            Enrollment.objects.create(
                student=user,
                subject=subject_obj,
                initial_marks=marks,
                starting_level=starting_level,
                current_level=starting_level,
                beginner_done=b_done,
                intermediate_done=i_done,
                advanced_done=a_done
            )

        login(request, user)
        messages.success(request, f"Welcome to the portal, {user.username}!")
        return redirect('student_dashboard')

    return render(request, 'accounts/student_signup.html', {'subjects': subjects})

def user_logout(request):
    logout(request)
    return redirect('landing')
