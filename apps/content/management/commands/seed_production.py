import csv
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import Project, NewsEvent, SuccessStory, FAQ


class Command(BaseCommand):
    help = 'Seed production data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

        if options['clear']:
            self.stdout.write('Clearing existing data...')
            FAQ.objects.all().delete()
            SuccessStory.objects.all().delete()
            NewsEvent.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write('Starting data seeding...')

        # Seed Projects
        self.seed_projects(data_dir)

        # Seed NewsEvents
        self.seed_news_events(data_dir)

        # Seed SuccessStories
        self.seed_success_stories(data_dir)

        # Seed FAQs
        self.seed_faqs(data_dir)

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))

    def seed_projects(self, data_dir):
        """Seed Project data from CSV"""
        csv_path = os.path.join(data_dir, '1_Project.csv')
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                application_deadline = self.parse_datetime(row.get('application_deadline'))
                start_date = self.parse_date(row.get('start_date'))
                end_date = self.parse_date(row.get('end_date'))
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean fields
                is_active = row.get('is_active', '').lower() == 'true'
                is_hero_highlight = row.get('is_hero_highlight', '').lower() == 'true'
                is_featured = row.get('is_featured', '').lower() == 'true'

                # Parse integers
                duration = int(row.get('duration', 0)) if row.get('duration') else 0
                headcount = int(row.get('headcount', 0)) if row.get('headcount') else 0
                total_headcount = int(row.get('total_headcount', 0)) if row.get('total_headcount') else 0

                project, created = Project.objects.get_or_create(
                    project_id=row.get('project_id'),
                    defaults={
                        'kicc_project_id': row.get('kicc_project_id') or None,
                        'title': row.get('title', ''),
                        'teaser': row.get('teaser', ''),
                        'background_objectives': row.get('background_objectives', ''),
                        'tasks_eligibility': row.get('tasks_eligibility', ''),
                        'country': row.get('country', ''),
                        'theme': row.get('theme', ''),
                        'duration': duration,
                        'difficulty': row.get('difficulty', ''),
                        'headcount': headcount,
                        'total_headcount': total_headcount,
                        'cover_image_url': row.get('cover_image_url') or None,
                        'application_deadline': application_deadline,
                        'start_date': start_date,
                        'end_date': end_date,
                        'is_active': is_active,
                        'is_hero_highlight': is_hero_highlight,
                        'is_featured': is_featured,
                        'created_at': created_at or timezone.now(),
                        'updated_at': updated_at or timezone.now(),
                    }
                )

                if created:
                    self.stdout.write(f'Created Project: {project.title}')
                else:
                    self.stdout.write(f'Project already exists: {project.title}')

    def seed_news_events(self, data_dir):
        """Seed NewsEvent data from CSV"""
        csv_path = os.path.join(data_dir, '2_NewsEvent.csv')
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                publish_date = self.parse_datetime(row.get('publish_date'))
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean fields
                is_published = row.get('is_published', '').lower() == 'true'
                is_hero_highlight = row.get('is_hero_highlight', '').lower() == 'true'
                is_featured = row.get('is_featured', '').lower() == 'true'

                news_event, created = NewsEvent.objects.get_or_create(
                    news_event_id=row.get('news_event_id'),
                    defaults={
                        'title': row.get('title', ''),
                        'body': row.get('body', ''),
                        'content_type': row.get('content_type', 'NEWS'),
                        'cover_image_url': row.get('cover_image_url') or '',
                        'external_link': row.get('external_link') or '',
                        'publish_date': publish_date or timezone.now(),
                        'is_published': is_published,
                        'is_hero_highlight': is_hero_highlight,
                        'is_featured': is_featured,
                        'created_at': created_at or timezone.now(),
                        'updated_at': updated_at or timezone.now(),
                    }
                )

                if created:
                    self.stdout.write(f'Created NewsEvent: {news_event.title}')
                else:
                    self.stdout.write(f'NewsEvent already exists: {news_event.title}')

    def seed_success_stories(self, data_dir):
        """Seed SuccessStory data from CSV"""
        csv_path = os.path.join(data_dir, '3_SuccessStory.csv')
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                published_at = self.parse_datetime(row.get('published_at'))
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean fields
                is_hero_highlight = row.get('is_hero_highlight', '').lower() == 'true'
                is_featured = row.get('is_featured', '').lower() == 'true'
                is_published = row.get('is_published', '').lower() == 'true'

                # Parse integers
                beneficiaries = int(row.get('beneficiaries', 0)) if row.get('beneficiaries') else None
                total_hours_contributed = int(row.get('total_hours_contributed', 0)) if row.get('total_hours_contributed') else None

                # Parse JSON fields
                image_urls = self.parse_json(row.get('image_urls', '[]'))
                video_urls = self.parse_json(row.get('video_urls', '[]'))

                # Handle related_project foreign key
                related_project = None
                if row.get('related_project'):
                    try:
                        related_project = Project.objects.get(project_id=row.get('related_project'))
                    except Project.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Related project not found: {row.get("related_project")}'))

                success_story, created = SuccessStory.objects.get_or_create(
                    success_story_id=row.get('success_story_id'),
                    defaults={
                        'title': row.get('title', ''),
                        'body': row.get('body', ''),
                        'related_project': related_project,
                        'cover_image_url': row.get('cover_image_url') or None,
                        'is_hero_highlight': is_hero_highlight,
                        'is_featured': is_featured,
                        'image_urls': image_urls,
                        'video_urls': video_urls,
                        'beneficiaries': beneficiaries,
                        'total_hours_contributed': total_hours_contributed,
                        'is_published': is_published,
                        'published_at': published_at or timezone.now(),
                        'created_at': created_at or timezone.now(),
                        'updated_at': updated_at or timezone.now(),
                    }
                )

                if created:
                    self.stdout.write(f'Created SuccessStory: {success_story.title}')
                else:
                    self.stdout.write(f'SuccessStory already exists: {success_story.title}')

    def seed_faqs(self, data_dir):
        """Seed FAQ data from CSV"""
        csv_path = os.path.join(data_dir, '4_FAQ.csv')
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean field
                is_schema_ready = row.get('is_schema_ready', '').lower() == 'true'

                # Parse integers
                order = int(row.get('order', 0)) if row.get('order') else 0
                thumbs_up = int(row.get('thumbs_up', 0)) if row.get('thumbs_up') else 0
                thumbs_down = int(row.get('thumbs_down', 0)) if row.get('thumbs_down') else 0

                faq, created = FAQ.objects.get_or_create(
                    faq_id=row.get('faq_id'),
                    defaults={
                        'question': row.get('question', ''),
                        'answer': row.get('answer', ''),
                        'order': order,
                        'is_schema_ready': is_schema_ready,
                        'thumbs_up': thumbs_up,
                        'thumbs_down': thumbs_down,
                        'created_at': created_at or timezone.now(),
                        'updated_at': updated_at or timezone.now(),
                    }
                )

                if created:
                    self.stdout.write(f'Created FAQ: {faq.question}')
                else:
                    self.stdout.write(f'FAQ already exists: {faq.question}')

    def parse_datetime(self, date_str):
        """Parse datetime string to datetime object"""
        if not date_str or date_str.lower() == 'null':
            return None
        try:
            # Handle ISO format with Z
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Make timezone-naive since USE_TZ=False
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            self.stdout.write(self.style.WARNING(f'Invalid datetime format: {date_str}'))
            return None

    def parse_date(self, date_str):
        """Parse date string to date object"""
        if not date_str or date_str.lower() == 'null':
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            self.stdout.write(self.style.WARNING(f'Invalid date format: {date_str}'))
            return None

    def parse_json(self, json_str):
        """Parse JSON string to Python object"""
        if not json_str:
            return []
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            self.stdout.write(self.style.WARNING(f'Invalid JSON: {json_str}'))
            return []
