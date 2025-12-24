from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Run all seed commands in sequence'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing data before seeding (passes to all seed commands)',
        )

    def handle(self, *args, **options):
        clear_flag = options.get('clear')
        
        seed_commands = [
            'seed_superuser',
            'seed_users',
            'seed_faqs',
            'seed_news',
            'seed_projects',
            'seed_stories',
            'seed_activities',
        ]

        if clear_flag:
            self.stdout.write(self.style.WARNING('🗑️  Clearing all database sequences...'))
            self._reset_auto_increment()
            self.stdout.write(self.style.SUCCESS('✓ All sequences reset'))
            self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('🌱 Starting master seed process...'))
        self.stdout.write('')

        for i, command in enumerate(seed_commands, 1):
            self.stdout.write(self.style.HTTP_INFO(f'[{i}/{len(seed_commands)}] Running {command}...'))
            
            try:
                call_args = {}
                if clear_flag:
                    call_args['clear'] = True
                
                call_command(command, **call_args)
                self.stdout.write(self.style.SUCCESS(f'✓ {command} completed successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ {command} failed: {str(e)}'))
                raise
            
            self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('🎉 All seed commands completed successfully!'))

    def _reset_auto_increment(self):
        """Reset all auto-increment sequences in the database"""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence")
