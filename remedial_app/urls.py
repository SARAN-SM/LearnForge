from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.landing_page, name='landing'),
    path('logout/', account_views.user_logout, name='logout'),
    path('student/', include('accounts.urls_student')),
    path('admin-portal/', include('accounts.urls_admin')),
    path('student/', include('students.urls')),
    path('admin-portal/', include('admin_portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
