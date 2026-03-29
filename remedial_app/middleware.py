from django.shortcuts import redirect
from django.urls import reverse

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        
        # Public routes
        public_routes = [
            '/', 
            '/student/login/', 
            '/student/signup/', 
            '/admin-portal/login/', 
            '/logout/'
        ]
        
        # Admin posting material triggers AI generator, could take time, but path is internal
        
        user = request.user
        
        # Static files & media skip
        if path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/'):
            return self.get_response(request)

        # Let public routes pass without redirect if not logged in
        # If logged in and hitting public routes, maybe redirect to dashboards
        if path in public_routes:
            if user.is_authenticated and path in ['/', '/student/login/', '/admin-portal/login/', '/student/signup/']:
                if getattr(user, 'role', '') == 'admin':
                    return redirect('/admin-portal/dashboard/')
                else:
                    return redirect('/student/dashboard/')
            return self.get_response(request)
        
        if not user.is_authenticated:
            # If they try to access student routes
            if path.startswith('/student/'):
                return redirect('/student/login/')
            # If they try to access admin routes
            if path.startswith('/admin-portal/'):
                return redirect('/admin-portal/login/')
            
            return redirect('/')

        # Access Control based on Roles
        role = getattr(user, 'role', '')
        
        if path.startswith('/student/') and role != 'student':
            return redirect('/logout/')
            
        if path.startswith('/admin-portal/') and role != 'admin':
            return redirect('/logout/')

        response = self.get_response(request)
        return response
