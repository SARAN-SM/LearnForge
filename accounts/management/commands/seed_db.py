from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Subject

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with explicit initial data'

    def handle(self, *args, **kwargs):
        # 1. Five subjects
        subjects = ['Mathematics', 'Science', 'English', 'History', 'Geography']
        for sub_name in subjects:
            Subject.objects.get_or_create(name=sub_name)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(subjects)} subjects.'))

        # 2. Two admin accounts
        admins = [
            {'username': 'admin', 'email': 'admin@school.com', 'password': 'Admin@123'},
            {'username': 'principal', 'email': 'principal@school.com', 'password': 'Admin@123'}
        ]

        for admin_data in admins:
            user, created = User.objects.get_or_create(
                username=admin_data['username'],
                defaults={'email': admin_data['email'], 'role': 'admin'}
            )
            if created:
                user.set_password(admin_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Admin user {user.username} already exists.'))
