from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.content.models import Project, NewsEvent, SuccessStory, SuccessStoryGalleryImage, ProjectGalleryImage, NewsEventGalleryImage, FAQ
from django.views.generic import TemplateView
from django.db.models import Count, Sum, Q, Max, Avg, F, ExpressionWrapper, FloatField, Case, When, Value
from django.utils import timezone
import logging
import mimetypes
import os
from datetime import timedelta
from apps.users.models import CustomUser
from django.db.models.functions import TruncMonth, TruncYear, TruncDay, TruncWeek
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SuccessStoryForm, ProjectForm, NewsEventForm, FAQForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


# --- Helper Functions ---
def handle_gallery_image_uploads(request, success_story_instance):
    """
    Helper function to handle multiple gallery image uploads for a success story.
    
    Args:
        request: The HTTP request object containing uploaded files
        success_story_instance: The SuccessStory instance to attach images to
    """
    if 'gallery_images' not in request.FILES:
        return
    
    files = request.FILES.getlist('gallery_images')
    
    # Get the current max order value for existing gallery images
    max_order = success_story_instance.gallery_images.aggregate(Max('order'))['order__max'] or -1
    
    for idx, uploaded_file in enumerate(files):
        # Read file data
        file_data = uploaded_file.read()
        
        # Get MIME type and filename
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        filename = os.path.basename(uploaded_file.name)
        
        # Create gallery image entry
        SuccessStoryGalleryImage.objects.create(
            success_story=success_story_instance,
            image_blob=file_data,
            image_blob_mime=mime_type or 'application/octet-stream',
            image_blob_name=filename,
            order=max_order + idx + 1
        )


def handle_project_gallery_image_uploads(request, project_instance):
    """
    Helper function to handle multiple gallery image uploads for a project.
    
    Args:
        request: The HTTP request object containing uploaded files
        project_instance: The Project instance to attach images to
    """
    if 'project_gallery_images' not in request.FILES:
        return
    
    files = request.FILES.getlist('project_gallery_images')
    
    # Get the current max order value for existing gallery images
    max_order = project_instance.gallery_images.aggregate(Max('order'))['order__max'] or -1
    
    for idx, uploaded_file in enumerate(files):
        # Read file data
        file_data = uploaded_file.read()
        
        # Get MIME type and filename
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        filename = os.path.basename(uploaded_file.name)
        
        # Create gallery image entry
        ProjectGalleryImage.objects.create(
            project=project_instance,
            image_blob=file_data,
            image_blob_mime=mime_type or 'application/octet-stream',
            image_blob_name=filename,
            order=max_order + idx + 1
        )


def handle_news_event_gallery_image_uploads(request, news_event_instance):
    """
    Helper function to handle multiple gallery image uploads for a news/event.
    
    Args:
        request: The HTTP request object containing uploaded files
        news_event_instance: The NewsEvent instance to attach images to
    """
    if 'news_event_gallery_images' not in request.FILES:
        return
    
    files = request.FILES.getlist('news_event_gallery_images')
    
    # Get the current max order value for existing gallery images
    max_order = news_event_instance.gallery_images.aggregate(Max('order'))['order__max'] or -1
    
    for idx, uploaded_file in enumerate(files):
        # Read file data
        file_data = uploaded_file.read()
        
        # Get MIME type and filename
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        filename = os.path.basename(uploaded_file.name)
        
        # Create gallery image entry
        NewsEventGalleryImage.objects.create(
            news_event=news_event_instance,
            image_blob=file_data,
            image_blob_mime=mime_type or 'application/octet-stream',
            image_blob_name=filename,
            order=max_order + idx + 1
        )


# --- Dashboard Views --- 
class DashboardDataView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    JSON API view to serve aggregated data for dashboard charts.
    Accepts GET parameters:
    - range: '30d', '90d', '6m', '1y', 'all'
    - frequency: 'day', 'week', 'month'
    """
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        range_param = request.GET.get('range', '6m')
        freq_param = request.GET.get('frequency', 'month')
        
        # Calculate start date
        today = timezone.now()
        start_date = today - timedelta(days=180) # Default 6m
        
        if range_param == '30d':
            start_date = today - timedelta(days=30)
        elif range_param == '90d':
            start_date = today - timedelta(days=90)
        elif range_param == '6m':
            start_date = today - timedelta(days=180)
        elif range_param == '1y':
            start_date = today - timedelta(days=365)
        elif range_param == 'all':
            start_date = today - timedelta(days=365*5) # Cap at 5 years for 'all' to avoid crazy loads
        
        # Determine Trunc function
        if freq_param == 'day':
            trunc_func = TruncDay
        elif freq_param == 'week':
            trunc_func = TruncWeek
        else:
            trunc_func = TruncMonth
            
        # 1. User Growth Over Time
        user_growth = (
            CustomUser.objects
            .filter(date_joined__gte=start_date)
            .annotate(period=trunc_func('date_joined'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )
        
        user_labels = [item['period'].strftime('%Y-%m-%d') for item in user_growth]
        user_data = [item['count'] for item in user_growth]
        
        # 2. Content Creation Activity (Stacked)
        # We need to normalize dates across all 3 content types
        projects = (
            Project.objects
            .filter(created_at__gte=start_date)
            .annotate(period=trunc_func('created_at'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )
        
        news = (
            NewsEvent.objects
            .filter(publish_date__gte=start_date)
            .annotate(period=trunc_func('publish_date'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )
        
        stories = (
            SuccessStory.objects
            .filter(published_at__gte=start_date)
            .annotate(period=trunc_func('published_at'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )
        
        # Create a set of all periods found
        all_periods = set()
        for qs in [projects, news, stories]:
            for item in qs:
                all_periods.add(item['period'])
        
        sorted_periods = sorted(list(all_periods))
        content_labels = [p.strftime('%Y-%m-%d') for p in sorted_periods]
        
        # Map data to periods
        def map_data(qs_data, periods):
            data_map = {item['period']: item['count'] for item in qs_data}
            return [data_map.get(p, 0) for p in periods]
            
        project_data = map_data(projects, sorted_periods)
        news_data = map_data(news, sorted_periods)
        story_data = map_data(stories, sorted_periods)
        
        # 3. Projects by Theme (Pie/Doughnut)
        themes = (
            Project.objects
            .filter(created_at__gte=start_date)
            .values('theme')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        theme_labels = [item['theme'] for item in themes]
        theme_data = [item['count'] for item in themes]
        
        # 4. Projects by Country (Bar)
        countries = (
            Project.objects
            .filter(created_at__gte=start_date)
            .values('country')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        country_labels = [item['country'] for item in countries]
        country_data = [item['count'] for item in countries]

        # 5. Beneficiaries Impact (Top 5 Projects created in range)
        top_projects_impact = (
             Project.objects
             .filter(created_at__gte=start_date, headcount__gt=0)
             .order_by('-headcount')[:5]
             .values('title', 'headcount')
        )
        impact_labels = [item['title'][:20] + '...' for item in top_projects_impact]
        impact_data = [item['headcount'] for item in top_projects_impact]
        
        data = {
            'user_growth': {
                'labels': user_labels,
                'data': user_data
            },
            'content_activity': {
                'labels': content_labels,
                'datasets': {
                    'projects': project_data,
                    'news': news_data,
                    'stories': story_data
                }
            },
            'themes': {
                'labels': theme_labels,
                'data': theme_data
            },
            'countries': {
                'labels': country_labels,
                'data': country_data
            },
            'impact': {
                'labels': impact_labels,
                'data': impact_data
            }
        }
        
        return JsonResponse(data)

class ManagementDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'content_management/management_dashboard.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- User Stats ---
        total_users = CustomUser.objects.count()
        new_users_30d = CustomUser.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=30)).count()
        active_users_30d = CustomUser.objects.filter(last_login__gte=timezone.now() - timezone.timedelta(days=30)).count()
        
        context['total_users'] = total_users
        context['new_users_30d'] = new_users_30d
        context['active_users_30d'] = active_users_30d
        # Avoid division by zero
        previous_users = total_users - new_users_30d
        context['user_growth_pct'] = round((new_users_30d / previous_users * 100), 1) if previous_users > 0 else 100

        # User Demographics
        context['users_by_gender'] = CustomUser.objects.values('gender').annotate(count=Count('id')).exclude(gender='').order_by('-count')
        context['users_by_country'] = CustomUser.objects.values('country_code').annotate(count=Count('id')).exclude(country_code='').order_by('-count')
        context['login_methods'] = CustomUser.objects.values('login_method').annotate(count=Count('id')).order_by('-count')
        context['onboarding_complete'] = CustomUser.objects.filter(onboarding_complete=True).count()
        context['email_verified'] = CustomUser.objects.filter(email_verified=True).count()
        context['onboarding_rate'] = round((context['onboarding_complete'] / total_users * 100), 1) if total_users > 0 else 0
        context['verification_rate'] = round((context['email_verified'] / total_users * 100), 1) if total_users > 0 else 0

        # --- Project Stats ---
        context['total_projects'] = Project.objects.count()
        context['active_projects'] = Project.objects.filter(is_active=True).count()
        context['completed_projects'] = Project.objects.filter(end_date__lt=timezone.now().date()).count()
        context['upcoming_projects'] = Project.objects.filter(start_date__gt=timezone.now().date()).count()
        context['featured_projects'] = Project.objects.filter(is_featured=True).count()
        context['hero_projects'] = Project.objects.filter(is_hero_highlight=True).count()
        
        # Capacity & Enrollment
        project_aggs = Project.objects.aggregate(
            total_capacity=Sum('total_headcount'),
            total_enrolled=Sum('headcount'),
            avg_duration=Avg(F('end_date') - F('start_date'))
        )
        context['total_capacity'] = project_aggs['total_capacity'] or 0
        context['total_enrolled'] = project_aggs['total_enrolled'] or 0
        context['utilization_rate'] = round((context['total_enrolled'] / context['total_capacity'] * 100), 1) if context['total_capacity'] > 0 else 0
        context['avg_project_duration'] = project_aggs['avg_duration'].days if project_aggs['avg_duration'] else 0

        # Unique enrolled users
        context['unique_enrolled_users'] = Project.objects.values('enrolled_users').distinct().count()

        # Upcoming deadlines
        context['upcoming_deadlines'] = Project.objects.filter(
            application_deadline__gte=timezone.now(),
            application_deadline__lte=timezone.now() + timezone.timedelta(days=30)
        ).count()

        # Breakdowns
        context['projects_by_difficulty'] = Project.objects.values('difficulty').annotate(count=Count('id')).order_by('-count')
        context['projects_by_theme'] = Project.objects.values('theme').annotate(count=Count('id')).order_by('-count')
        context['projects_by_country'] = Project.objects.values('country').annotate(count=Count('id')).order_by('-count')

        # --- News & Events ---
        context['total_news_events'] = NewsEvent.objects.count()
        context['published_news_events'] = NewsEvent.objects.filter(is_published=True).count()
        context['news_count'] = NewsEvent.objects.filter(content_type='News').count()
        context['event_count'] = NewsEvent.objects.filter(content_type='Event').count()
        context['featured_news'] = NewsEvent.objects.filter(is_featured=True).count()
        context['hero_news'] = NewsEvent.objects.filter(is_hero_highlight=True).count()

        # --- Success Stories & Impact ---
        context['total_success_stories'] = SuccessStory.objects.count()
        context['published_stories'] = SuccessStory.objects.filter(is_published=True).count()
        context['featured_stories'] = SuccessStory.objects.filter(is_featured=True).count()
        context['hero_stories'] = SuccessStory.objects.filter(is_hero_highlight=True).count()
        
        impact_aggs = SuccessStory.objects.aggregate(
            total_beneficiaries=Sum('beneficiaries'),
            total_hours=Sum('total_hours_contributed'),
            avg_beneficiaries=Avg('beneficiaries'),
            avg_hours=Avg('total_hours_contributed')
        )
        context['total_beneficiaries'] = impact_aggs['total_beneficiaries'] or 0
        context['total_hours_contributed'] = impact_aggs['total_hours'] or 0
        context['avg_beneficiaries_per_story'] = round(impact_aggs['avg_beneficiaries'] or 0, 1)
        context['avg_hours_per_story'] = round(impact_aggs['avg_hours'] or 0, 1)
        
        # --- FAQs ---
        context['total_faqs'] = FAQ.objects.count()

        # --- Gallery Images ---
        context['total_project_gallery_images'] = ProjectGalleryImage.objects.count()
        context['total_success_story_gallery_images'] = SuccessStoryGalleryImage.objects.count()
        context['total_news_event_gallery_images'] = NewsEventGalleryImage.objects.count()
        context['total_gallery_images'] = (
            context['total_project_gallery_images'] + 
            context['total_success_story_gallery_images'] + 
            context['total_news_event_gallery_images']
        )

        # --- Recent Content ---
        context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        context['recent_news_events'] = NewsEvent.objects.order_by('-publish_date')[:5]
        context['recent_success_stories'] = SuccessStory.objects.order_by('-published_at')[:5]
        
        # --- Chart Data Preparation ---
        # 1. Content Distribution (Pie Chart)
        context['chart_labels'] = ['Projects', 'News & Events', 'Success Stories', 'FAQs']
        context['chart_data'] = [
            context['total_projects'], 
            context['total_news_events'], 
            context['total_success_stories'], 
            context['total_faqs']
        ]

        # 2. Monthly Activity (Line Chart) - Last 6 Months
        today = timezone.now()
        months = []
        project_counts = []
        news_counts = []
        
        # Simple loop for last 6 months
        for i in range(5, -1, -1):
            # Calculate start of month
            month_date = today - timezone.timedelta(days=i*30) 
            month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate end of month (start of next month)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year+1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month+1)
            
            months.append(month_start.strftime('%b'))
            project_counts.append(Project.objects.filter(created_at__gte=month_start, created_at__lt=month_end).count())
            news_counts.append(NewsEvent.objects.filter(publish_date__gte=month_start, publish_date__lt=month_end).count())

        context['activity_months'] = months
        context['activity_project_data'] = project_counts
        context['activity_news_data'] = news_counts

        return context


class UserAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'content_management/user_analytics.html'
    context_object_name = 'viewed_users'
    paginate_by = 20
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = CustomUser.objects.all()

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(country_code__icontains=search_query)
            )

        # Sorting functionality
        sort_by = self.request.GET.get('sort', '-date_joined')
        valid_sort_fields = {
            'username': 'username',
            '-username': '-username',
            'email': 'email',
            '-email': '-email',
            'first_name': 'first_name',
            '-first_name': '-first_name',
            'last_name': 'last_name',
            '-last_name': '-last_name',
            'country_code': 'country_code',
            '-country_code': '-country_code',
            'date_joined': 'date_joined',
            '-date_joined': '-date_joined',
            'is_active': 'is_active',
            '-is_active': '-is_active',
        }

        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(valid_sort_fields[sort_by])
        else:
            queryset = queryset.order_by('-date_joined')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-date_joined')

        # Total Users
        context['total_users'] = CustomUser.objects.count()

        # New Users Over Time (Monthly)
        context['users_by_month'] = (
            CustomUser.objects
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # New Users Over Time (Yearly)
        context['users_by_year'] = (
            CustomUser.objects
            .annotate(year=TruncYear('date_joined'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        # User Demographics
        context['users_by_gender'] = CustomUser.objects.values('gender').annotate(count=Count('gender')).order_by('-count')
        context['users_by_country'] = CustomUser.objects.values('country_code').annotate(count=Count('country_code')).order_by('-count')

        # Active Users (users who have enrolled in projects)
        context['active_users'] = CustomUser.objects.filter(enrolled_projects__isnull=False).distinct().count()

        return context

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    context_object_name = 'viewed_user'
    template_name = 'content_management/user_form.html'
    fields = [
        'username', 'email', 'first_name', 'last_name',
        'date_of_birth', 'gender', 'blood_group', 'guardian_name',
        'guardian_relation', 'address', 'contact', 'country_code',
        'is_active', 'is_staff', 'is_superuser'
    ]
    success_url = reverse_lazy('user_analytics')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)
    
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    context_object_name = 'viewed_user'
    template_name = 'content_management/user_form.html'
    fields = [
        'username', 'email', 'first_name', 'last_name',
        'date_of_birth', 'gender', 'blood_group', 'guardian_name',
        'guardian_relation', 'address', 'contact', 'country_code',
        'is_active', 'is_staff', 'is_superuser'
    ]
    success_url = reverse_lazy('user_analytics')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'content_management/user_detail.html'
    context_object_name = 'viewed_user'
    queryset = CustomUser.objects.all()
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'content_management/user_confirm_delete.html'
    context_object_name = 'viewed_user'
    success_url = reverse_lazy('user_analytics')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff


class ApplicationAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'content_management/application_analytics.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Project Enrollment Stats
        context['total_enrollments'] = Project.objects.aggregate(total=Sum('headcount'))['total'] or 0
        context['projects_with_enrollments'] = Project.objects.filter(headcount__gt=0).count()

        # Popular Projects (by enrollment)
        context['popular_projects'] = Project.objects.filter(headcount__gt=0).order_by('-headcount')[:10]

        # Projects by Theme with enrollment counts
        context['enrollments_by_theme'] = (
            Project.objects
            .values('theme')
            .annotate(total_enrollments=Sum('headcount'), project_count=Count('id'))
            .order_by('-total_enrollments')
        )

        # Projects by Country with enrollment counts
        context['enrollments_by_country'] = (
            Project.objects
            .values('country')
            .annotate(total_enrollments=Sum('headcount'), project_count=Count('id'))
            .order_by('-total_enrollments')
        )

        # Project Capacity Utilization
        projects = Project.objects.filter(total_headcount__gt=0).exclude(total_headcount__isnull=True)
        context['capacity_data'] = [
            {
                'pk': p.pk,
                'title': p.title,
                'utilization': (p.headcount / p.total_headcount * 100) if p.total_headcount > 0 else 0,
                'enrolled': p.headcount,
                'capacity': p.total_headcount
            } for p in projects if p.pk
        ][:10]  # Top 10

        # Recent Enrollments (projects with recent enrollment activity)
        context['recent_enrollments'] = Project.objects.filter(headcount__gt=0).order_by('-updated_at')[:10]

        return context



# --- Project Views ---
class ProjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 15
    model = Project
    template_name = 'content_management/project_list.html'
    context_object_name = 'projects'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = Project.objects.all()

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(theme__icontains=search_query) |
                Q(teaser__icontains=search_query) |
                Q(background_objectives__icontains=search_query)
            )

        # Sorting functionality
        sort_by = self.request.GET.get('sort', '-created_at')
        valid_sort_fields = {
            'title': 'title',
            '-title': '-title',
            'country': 'country',
            '-country': '-country',
            'theme': 'theme',
            '-theme': '-theme',
            'headcount': 'headcount',
            '-headcount': '-headcount',
            'is_active': 'is_active',
            '-is_active': '-is_active',
            'created_at': 'created_at',
            '-created_at': '-created_at',
            'start_date': 'start_date',
            '-start_date': '-start_date',
        }

        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(valid_sort_fields[sort_by])
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'content_management/project_detail.html'
    context_object_name = 'project'
    queryset = Project.objects.all()
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        
        # Create unified gallery items list combining all content types
        gallery_items = []
        index = 0
        
        # Add blob images
        for gallery_image in project.gallery_images.all().order_by('order'):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': index
            })
            index += 1
        
        # Add image URLs
        for image_url in project.image_urls:
            gallery_items.append({
                'type': 'image_url',
                'url': image_url,
                'index': index
            })
            index += 1
        
        # Add video URLs
        for video_url in project.video_urls:
            gallery_items.append({
                'type': 'video_url',
                'url': video_url,
                'index': index
            })
            index += 1
        
        # Paginate the unified gallery items
        from django.core.paginator import Paginator
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
        return context

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name = 'content_management/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Process video and image URLs from form arrays
        video_urls = self.request.POST.getlist('video_urls[]')
        image_urls = self.request.POST.getlist('image_urls[]')
        
        # Filter out empty strings and save to model
        form.instance.video_urls = [url for url in video_urls if url.strip()]
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        
        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_project_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'content_management/project_form.html'
    context_object_name = 'project'
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Process video and image URLs from form arrays
        video_urls = self.request.POST.getlist('video_urls[]')
        image_urls = self.request.POST.getlist('image_urls[]')
        
        # Filter out empty strings and save to model
        form.instance.video_urls = [url for url in video_urls if url.strip()]
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        
        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_project_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'content_management/project_confirm_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

# --- NewsEvent Views ---
class NewsEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 15
    model = NewsEvent
    template_name = 'content_management/news_event_list.html'
    context_object_name = 'news_events'
    queryset = NewsEvent.objects.all().order_by('-publish_date')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', '-publish_date')

        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(content_type__icontains=search_query)
            )

        # Apply sorting
        allowed_sort_fields = {
            'title': 'title',
            '-title': '-title',
            'content_type': 'content_type',
            '-content_type': '-content_type',
            'publish_date': 'publish_date',
            '-publish_date': '-publish_date',
            'is_published': 'is_published',
            '-is_published': '-is_published',
        }

        if sort_by in allowed_sort_fields:
            queryset = queryset.order_by(allowed_sort_fields[sort_by])
        else:
            queryset = queryset.order_by('-publish_date')  # Default sorting

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-publish_date')
        return context

class NewsEventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = NewsEvent
    template_name = 'content_management/news_event_detail.html'
    context_object_name = 'news_event'
    queryset = NewsEvent.objects.all()
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_event = self.object
        
        # Create unified gallery items list combining all content types
        gallery_items = []
        index = 0
        
        # Add blob images
        for gallery_image in news_event.gallery_images.all().order_by('order'):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': index
            })
            index += 1
        
        # Add image URLs
        for image_url in news_event.image_urls:
            gallery_items.append({
                'type': 'image_url',
                'url': image_url,
                'index': index
            })
            index += 1
        
        # Add video URLs
        for video_url in news_event.video_urls:
            gallery_items.append({
                'type': 'video_url',
                'url': video_url,
                'index': index
            })
            index += 1
        
        # Paginate the unified gallery items
        from django.core.paginator import Paginator
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
        return context

class NewsEventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = NewsEvent
    template_name = 'content_management/news_event_form.html'
    form_class = NewsEventForm
    success_url = reverse_lazy('news_event_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Handle video and image URLs
        video_urls = self.request.POST.getlist('video_urls[]')
        image_urls = self.request.POST.getlist('image_urls[]')

        form.instance.video_urls = [url for url in video_urls if url.strip()]
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        
        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_news_event_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class NewsEventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsEvent
    template_name = 'content_management/news_event_form.html'
    context_object_name = 'news_event'
    form_class = NewsEventForm
    success_url = reverse_lazy('news_event_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Handle video and image URLs
        video_urls = self.request.POST.getlist('video_urls[]')
        image_urls = self.request.POST.getlist('image_urls[]')

        form.instance.video_urls = [url for url in video_urls if url.strip()]
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        
        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_news_event_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class NewsEventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsEvent
    template_name = 'content_management/news_event_confirm_delete.html'
    context_object_name = 'news_event'
    success_url = reverse_lazy('news_event_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

# --- SuccessStory Views ---
class SuccessStoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 15
    model = SuccessStory
    template_name = 'content_management/success_story_list.html'
    context_object_name = 'success_stories'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = SuccessStory.objects.select_related('related_project').all()

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(related_project__title__icontains=search_query) |
                Q(body__icontains=search_query)
            )

        # Sorting functionality
        sort_by = self.request.GET.get('sort', '-published_at')
        valid_sort_fields = {
            'title': 'title',
            '-title': '-title',
            'published_at': 'published_at',
            '-published_at': '-published_at',
            'related_project': 'related_project__title',
            '-related_project': '-related_project__title',
            'is_published': 'is_published',
            '-is_published': '-is_published',
        }

        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(valid_sort_fields[sort_by])
        else:
            queryset = queryset.order_by('-published_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-published_at')
        return context

class SuccessStoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SuccessStory
    template_name = 'content_management/success_story_detail.html'
    context_object_name = 'success_story'
    queryset = SuccessStory.objects.all()
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_story = self.object
        
        # Create unified gallery items list combining all content types
        gallery_items = []
        index = 0
        
        # Add blob images
        for gallery_image in success_story.gallery_images.all().order_by('order'):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': index
            })
            index += 1
        
        # Add image URLs
        for image_url in success_story.image_urls:
            gallery_items.append({
                'type': 'image_url',
                'url': image_url,
                'index': index
            })
            index += 1
        
        # Add video URLs
        for video_url in success_story.video_urls:
            gallery_items.append({
                'type': 'video_url',
                'url': video_url,
                'index': index
            })
            index += 1
        
        # Paginate the unified gallery items
        from django.core.paginator import Paginator
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
        return context

class SuccessStoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SuccessStory
    template_name = 'content_management/success_story_form.html'
    form_class = SuccessStoryForm
    success_url = reverse_lazy('success_story_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Process multiple image and video URLs from form arrays
        image_urls = self.request.POST.getlist('image_urls[]')
        video_urls = self.request.POST.getlist('video_urls[]')

        # Filter out empty strings and save to model
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        form.instance.video_urls = [url for url in video_urls if url.strip()]

        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class SuccessStoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SuccessStory
    template_name = 'content_management/success_story_form.html'
    context_object_name = 'success_story' # Ensure the object is available as 'success_story' in the template
    form_class = SuccessStoryForm
    success_url = reverse_lazy('success_story_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        # Process multiple image and video URLs from form arrays
        image_urls = self.request.POST.getlist('image_urls[]')
        video_urls = self.request.POST.getlist('video_urls[]')

        # Filter out empty strings and save to model
        form.instance.image_urls = [url for url in image_urls if url.strip()]
        form.instance.video_urls = [url for url in video_urls if url.strip()]

        # Save the form first
        response = super().form_valid(form)
        
        # Handle multiple gallery image uploads using helper function
        handle_gallery_image_uploads(self.request, form.instance)
        
        return response

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class SuccessStoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SuccessStory
    template_name = 'content_management/success_story_confirm_delete.html'
    context_object_name = 'success_story'
    success_url = reverse_lazy('success_story_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

# --- FAQ Views ---
class FAQListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 15
    model = FAQ
    template_name = 'content_management/faq_list.html'
    context_object_name = 'faqs'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = FAQ.objects.annotate(
            total_votes_cnt=F('thumbs_up') + F('thumbs_down')
        ).annotate(
            usefulness=Case(
                When(total_votes_cnt__gt=0, then=ExpressionWrapper(
                    F('thumbs_up') * 100.0 / F('total_votes_cnt'),
                    output_field=FloatField()
                )),
                default=Value(0.0),
                output_field=FloatField()
            )
        )

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(question__icontains=search_query) |
                Q(answer__icontains=search_query)
            )

        # Sorting functionality
        sort_by = self.request.GET.get('sort', 'order')
        valid_sort_fields = {
            'order': 'order',
            '-order': '-order',
            'question': 'question',
            '-question': '-question',
            'is_schema_ready': 'is_schema_ready',
            '-is_schema_ready': '-is_schema_ready',
            'thumbs_up': 'thumbs_up',
            '-thumbs_up': '-thumbs_up',
            'thumbs_down': 'thumbs_down',
            '-thumbs_down': '-thumbs_down',
            'usefulness': 'usefulness',
            '-usefulness': '-usefulness',
        }

        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(valid_sort_fields[sort_by])
        else:
            queryset = queryset.order_by('order')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'order')
        return context

class FAQDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = FAQ
    template_name = 'content_management/faq_detail.html'
    context_object_name = 'faq'
    queryset = FAQ.objects.all()
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

class FAQCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FAQ
    template_name = 'content_management/faq_form.html'
    form_class = FAQForm
    success_url = reverse_lazy('faq_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class FAQUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FAQ
    template_name = 'content_management/faq_form.html'
    form_class = FAQForm
    success_url = reverse_lazy('faq_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class FAQDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FAQ
    template_name = 'content_management/faq_confirm_delete.html'
    context_object_name = 'faq'
    success_url = reverse_lazy('faq_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff
