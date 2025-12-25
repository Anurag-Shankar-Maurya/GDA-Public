from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from apps.users.models import CustomUser, Certificate
from apps.content.models import Project, FAQ, FAQVote
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed user activities including enrollments, certificates, FAQ votes, and more'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing activity data before seeding',
        )

    def handle(self, *args, **options):
        if options.get('clear'):
            self.stdout.write(self.style.WARNING('Clearing existing activity data...'))
            Certificate.objects.all().delete()
            FAQVote.objects.all().delete()
            
            # Clear enrolled_users relationships
            for project in Project.objects.all():
                project.enrolled_users.clear()
            
            self.stdout.write(self.style.SUCCESS('Cleared all existing activities'))
            
            # Reset auto-increment IDs
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='users_certificate'")
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='content_faqvote'")
        
        # Get all users and projects
        users = list(CustomUser.objects.exclude(username='admin').all())
        projects = list(Project.objects.all())
        faqs = list(FAQ.objects.all())
        
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Run seed_users first.'))
            return
        
        if not projects:
            self.stdout.write(self.style.WARNING('No projects found. Run seed_projects first.'))
            return
        
        enrollments_count = 0
        certificates_count = 0
        faq_votes_count = 0
        
        self.stdout.write(self.style.SUCCESS('🚀 Starting activity seeding...'))
        self.stdout.write('')
        
        # 1. Create enrollments (users signing up for projects)
        self.stdout.write('📝 Creating project enrollments...')
        for user in users:
            # Randomly assign 2-6 projects to each user
            num_projects = random.randint(2, min(6, len(projects)))
            assigned_projects = random.sample(projects, num_projects)
            
            for project in assigned_projects:
                try:
                    project.enrolled_users.add(user)
                    enrollments_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to enroll {user.username} in project {project.id}: {str(e)}'
                        )
                    )
                    continue
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {enrollments_count} project enrollments')
        )
        
        # 2. Create certificates (completion records)
        self.stdout.write('🏆 Creating completion certificates...')
        for user in users:
            # 40-70% of enrolled projects are completed
            enrolled_projects = list(user.enrolled_projects.all())
            num_completed = int(len(enrolled_projects) * random.uniform(0.4, 0.7))
            completed_projects = random.sample(enrolled_projects, num_completed)
            
            for project in completed_projects:
                try:
                    # Issue certificate in the past (1-365 days ago)
                    issued_date = timezone.now() - timedelta(days=random.randint(1, 365))
                    certificate, created = Certificate.objects.get_or_create(
                        user=user,
                        project=project,
                        defaults={'issued_at': issued_date}
                    )
                    if created:
                        certificates_count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to create certificate for {user.username} on project {project.id}: {str(e)}'
                        )
                    )
                    continue
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Created {certificates_count} completion certificates')
        )
        
        # 3. Create FAQ votes (user engagement)
        self.stdout.write('👍 Creating FAQ votes...')
        if faqs:
            for user in users:
                # 30-60% of users vote on FAQs
                if random.random() > 0.5:
                    # Each voting user votes on 3-8 FAQs
                    num_votes = random.randint(3, min(8, len(faqs)))
                    voted_faqs = random.sample(faqs, num_votes)
                    
                    for faq in voted_faqs:
                        try:
                            vote_type = random.choice([
                                FAQVote.VoteType.UP,
                                FAQVote.VoteType.DOWN
                            ])
                            faq_vote, created = FAQVote.objects.get_or_create(
                                user=user,
                                faq=faq,
                                defaults={
                                    'vote_type': vote_type,
                                    'created_at': timezone.now() - timedelta(days=random.randint(1, 365))
                                }
                            )
                            if created:
                                faq_votes_count += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Failed to create FAQ vote for {user.username} on FAQ {faq.id}: {str(e)}'
                                )
                            )
                            continue
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created {faq_votes_count} FAQ votes')
            )
        else:
            self.stdout.write(self.style.WARNING('No FAQs found. Skipping FAQ votes.'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 Activity seeding completed!'))
        self.stdout.write(self.style.HTTP_INFO(f'   📝 Enrollments: {enrollments_count}'))
        self.stdout.write(self.style.HTTP_INFO(f'   🏆 Certificates: {certificates_count}'))
        self.stdout.write(self.style.HTTP_INFO(f'   👍 FAQ Votes: {faq_votes_count}'))
        self.stdout.write(self.style.HTTP_INFO(f'   📊 Total Activities: {enrollments_count + certificates_count + faq_votes_count}'))
