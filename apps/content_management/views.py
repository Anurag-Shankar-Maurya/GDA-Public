from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.content.models import Project, NewsEvent, SuccessStory, FAQ
from django.views.generic import TemplateView
from django.db.models import Count, Sum, Q
from django.utils import timezone
import logging
from apps.users.models import CustomUser
from django.db.models.functions import TruncMonth, TruncYear
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)

# --- Dashboard Views --- 
class ManagementDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'content_management/management_dashboard.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Summary Cards Data
        context['total_projects'] = Project.objects.count()
        context['active_projects'] = Project.objects.filter(is_active=True).count()
        context['total_news_events'] = NewsEvent.objects.count()
        context['total_success_stories'] = SuccessStory.objects.count()
        context['total_faqs'] = FAQ.objects.count()

        # Content Performance (Example: Projects by Theme)
        context['projects_by_theme'] = Project.objects.values('theme').annotate(count=Count('theme')).order_by('-count')

        # User Engagement (Example: Success Stories with beneficiaries and hours)
        context['total_beneficiaries'] = SuccessStory.objects.aggregate(Sum('beneficiaries'))['beneficiaries__sum'] or 0
        context['total_hours_contributed'] = SuccessStory.objects.aggregate(Sum('total_hours_contributed'))['total_hours_contributed__sum'] or 0

        # Recent Content
        context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        context['recent_news_events'] = NewsEvent.objects.order_by('-publish_date')[:5]
        context['recent_success_stories'] = SuccessStory.objects.order_by('-published_at')[:5]

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

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name = 'content_management/project_form.html'
    fields = '__all__'
    success_url = reverse_lazy('project_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'content_management/project_form.html'
    context_object_name = 'project'
    fields = '__all__'
    success_url = reverse_lazy('project_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

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

class NewsEventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = NewsEvent
    template_name = 'content_management/news_event_form.html'
    fields = '__all__'
    success_url = reverse_lazy('news_event_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class NewsEventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsEvent
    template_name = 'content_management/news_event_form.html'
    context_object_name = 'news_event'
    fields = '__all__'
    success_url = reverse_lazy('news_event_list')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

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

class SuccessStoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SuccessStory
    template_name = 'content_management/success_story_form.html'
    # For ForeignKey, Django's default form generation works well if the related model is also managed.
    fields = '__all__'
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

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"Form has errors: {form.errors.as_json()}")
        return super().form_invalid(form)

class SuccessStoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SuccessStory
    template_name = 'content_management/success_story_form.html'
    context_object_name = 'success_story' # Ensure the object is available as 'success_story' in the template
    fields = '__all__'
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

        return super().form_valid(form)

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
    queryset = FAQ.objects.all().order_by('order')
    login_url = '/login/'
    redirect_field_name = 'next'

    def test_func(self):
        return self.request.user.is_staff

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
    fields = '__all__'
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
    fields = '__all__'
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

