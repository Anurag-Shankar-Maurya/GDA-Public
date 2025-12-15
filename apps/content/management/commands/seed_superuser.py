from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Create a superuser, a staff user, and a superuser-only user with specified details'

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser, staff user, and superuser-only user...')

        # Create superuser
        superuser_data = {
            'username': 'anurag',
            'email': 'anuragmaurya3233@gmail.com',
            'first_name': 'Anurag',
            'last_name': 'Maurya',
            'date_of_birth': date(1990, 1, 1),  # Dummy date
            'gender': 'Male',
            'blood_group': 'O+',  # Dummy
            'guardian_name': 'Dummy Guardian',  # Dummy
            'guardian_relation': 'Father',  # Dummy
            'address': 'Dummy Address, City, Country',  # Dummy
            'contact': '1234567890',  # Dummy
            'country_code': '+91',  # Dummy
        }

        superuser, created = CustomUser.objects.get_or_create(
            username=superuser_data['username'],
            defaults=superuser_data
        )

        if created:
            superuser.set_password('BabuBhaiya3233..')
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser {superuser.username} created successfully!'))
        else:
            self.stdout.write(f'Superuser {superuser.username} already exists')

        # Create staff user
        staff_data = {
            'username': 'manager',
            'email': 'manager@gmail.com',
            'first_name': 'Manager',  # Dummy
            'last_name': 'User',  # Dummy
            'date_of_birth': date(1985, 5, 15),  # Dummy date
            'gender': 'Male',  # Dummy
            'blood_group': 'A+',  # Dummy
            'guardian_name': 'Dummy Guardian',  # Dummy
            'guardian_relation': 'Father',  # Dummy
            'address': 'Dummy Address, City, Country',  # Dummy
            'contact': '0987654321',  # Dummy
            'country_code': '+91',  # Dummy
        }

        staff, created = CustomUser.objects.get_or_create(
            username=staff_data['username'],
            defaults=staff_data
        )

        if created:
            staff.set_password('GDAmanager3233..')
            staff.is_staff = True
            staff.is_superuser = False
            staff.save()
            self.stdout.write(self.style.SUCCESS(f'Staff user {staff.username} created successfully!'))
        else:
            self.stdout.write(f'Staff user {staff.username} already exists')

        # Create superuser-only user
        superuser_only_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'first_name': 'Admin',  # Dummy
            'last_name': 'User',  # Dummy
            'date_of_birth': date(1980, 10, 10),  # Dummy date
            'gender': 'Male',  # Dummy
            'blood_group': 'B+',  # Dummy
            'guardian_name': 'Dummy Guardian',  # Dummy
            'guardian_relation': 'Father',  # Dummy
            'address': 'Dummy Address, City, Country',  # Dummy
            'contact': '1122334455',  # Dummy
            'country_code': '+91',  # Dummy
        }

        superuser_only, created = CustomUser.objects.get_or_create(
            username=superuser_only_data['username'],
            defaults=superuser_only_data
        )

        if created:
            superuser_only.set_password('AdminPass123..')
            superuser_only.is_staff = False
            superuser_only.is_superuser = True
            superuser_only.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser-only user {superuser_only.username} created successfully!'))
        else:
            self.stdout.write(f'Superuser-only user {superuser_only.username} already exists')