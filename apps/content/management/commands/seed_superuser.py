from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from datetime import date
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Create a superuser, a staff user, and a superuser-only user with specified details'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing users before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser, staff user, and superuser-only user...')

        if options.get('clear'):
            CustomUser.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing users'))
            
            # Reset auto-increment ID
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='users_customuser'")

        # Create superuser
        superuser_data = {
            'username': 'anurag',
            'email': 'anuragmaurya3233@gmail.com',
            'first_name': 'Anurag',
            'last_name': 'Maurya',
            'date_of_birth': date(1990, 5, 15),
            'gender': 'Male',
            'blood_group': 'O+',
            'guardian_name': 'Kapil Maurya',
            'guardian_relation': 'Father',
            'address': '123 Admin Street, New Delhi, India',
            'contact': '+919876543210',
            'country_code': 'IN',
            'login_method': 'email',
            'onboarding_complete': True,
            'email_verified': True,
            'is_active': True,
        }

        superuser, created = CustomUser.objects.get_or_create(
            username=superuser_data['username'],
            defaults=superuser_data
        )

        if created:
            superuser.set_password('BabuBhaiya3233..')
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.onboarding_complete = True
            superuser.email_verified = True
            superuser.is_active = True
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser {superuser.username} created successfully!'))
        else:
            self.stdout.write(f'Superuser {superuser.username} already exists')

        # Create staff user
        staff_data = {
            'username': 'manager',
            'email': 'manager@gda-volunteer.org',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'date_of_birth': date(1988, 3, 22),
            'gender': 'Female',
            'blood_group': 'A+',
            'guardian_name': 'Vikram Sharma',
            'guardian_relation': 'Father',
            'address': '456 Management Avenue, Mumbai, India',
            'contact': '+919123456789',
            'country_code': 'IN',
            'login_method': 'email',
            'onboarding_complete': True,
            'email_verified': True,
            'is_active': True,
        }

        staff, created = CustomUser.objects.get_or_create(
            username=staff_data['username'],
            defaults=staff_data
        )

        if created:
            staff.set_password('GDAmanager3233..')
            staff.is_staff = True
            staff.is_superuser = False
            staff.onboarding_complete = True
            staff.email_verified = True
            staff.is_active = True
            staff.save()
            self.stdout.write(self.style.SUCCESS(f'Staff user {staff.username} created successfully!'))
        else:
            self.stdout.write(f'Staff user {staff.username} already exists')

        # Create superuser-only user
        superuser_only_data = {
            'username': 'admin',
            'email': 'admin@gda-volunteer.org',
            'first_name': 'Rahul',
            'last_name': 'Verma',
            'date_of_birth': date(1985, 7, 10),
            'gender': 'Male',
            'blood_group': 'B+',
            'guardian_name': 'Suresh Verma',
            'guardian_relation': 'Father',
            'address': '789 Administrative Complex, Bangalore, India',
            'contact': '+919988776655',
            'country_code': 'IN',
            'login_method': 'email',
            'onboarding_complete': True,
            'email_verified': True,
            'is_active': True,
        }

        superuser_only, created = CustomUser.objects.get_or_create(
            username=superuser_only_data['username'],
            defaults=superuser_only_data
        )

        if created:
            superuser_only.set_password('AdminPass123..')
            superuser_only.is_staff = False
            superuser_only.is_superuser = True
            superuser_only.onboarding_complete = True
            superuser_only.email_verified = True
            superuser_only.is_active = True
            superuser_only.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser-only user {superuser_only.username} created successfully!'))
        else:
            self.stdout.write(f'Superuser-only user {superuser_only.username} already exists')