from django.shortcuts import render, redirect

def landing_page(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'role', '') == 'admin':
            return redirect('admin_dashboard')
        elif getattr(request.user, 'role', '') == 'student':
            return redirect('student_dashboard')
    
    return render(request, 'landing.html')
