from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Project, NewsEvent, SuccessStory, FAQ
import json
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

_BLOB_MODEL_MAP = {
    'project': Project,
    'news_event': NewsEvent,
    'success_story': SuccessStory,
}

# Project Views
class ProjectListView(ListView):
    model = Project
    template_name = 'content/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True)
        # Filtering
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country__icontains=country)
        theme = self.request.GET.get('theme')
        if theme:
            queryset = queryset.filter(theme__icontains=theme)
        duration = self.request.GET.get('duration')
        if duration:
            queryset = queryset.filter(duration=duration)
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        # Searching
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(teaser__icontains=search) |
                Q(background_objectives__icontains=search) |
                Q(tasks_eligibility__icontains=search)
            )
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_projects = Project.objects.filter(is_active=True)
        # Get hero projects for the carousel
        context['hero_projects'] = active_projects.filter(is_hero_highlight=True).order_by('-created_at')[:3]
        # Get featured projects
        context['featured_projects'] = active_projects.filter(is_featured=True).order_by('-created_at')[:3]
        context['countries'] = sorted(set(active_projects.values_list('country', flat=True)))
        context['themes'] = sorted(set(active_projects.values_list('theme', flat=True)))
        context['durations'] = sorted(set(active_projects.values_list('duration', flat=True)))
        context['difficulties'] = ['Easy', 'Medium', 'Hard']
        context['sort_options'] = [
            {'value': '-created_at', 'label': _('Newest First')},
            {'value': 'created_at', 'label': _('Oldest First')},
            {'value': 'duration', 'label': _('Duration (Low to High)')},
            {'value': '-duration', 'label': _('Duration (High to Low)')},
            {'value': 'difficulty', 'label': _('Difficulty (Easy to Hard)')},
            {'value': '-difficulty', 'label': _('Difficulty (Hard to Easy)')},
            {'value': 'title', 'label': _('Title (A-Z)')},
            {'value': '-title', 'label': _('Title (Z-A)')},
        ]
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'content/project_detail.html'
    context_object_name = 'project'
    queryset = Project.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        user = self.request.user
        context['can_apply'] = project.can_user_apply(user)
        context['is_enrolled'] = user.is_authenticated and project.enrolled_users.filter(id=user.id).exists()
        
        # Related success stories for this project
        context['related_success_stories'] = SuccessStory.objects.filter(
            related_project=project,
            is_published=True
        ).order_by('-published_at')[:3]
        
        # Related projects with smart filtering logic
        # Priority 1: Same theme AND same country (closest match)
        related_projects = Project.objects.filter(
            theme=project.theme,
            country=project.country,
            is_active=True
        ).exclude(pk=project.pk).order_by('-created_at')[:3]
        
        # Priority 2: If not enough results, get projects with same theme
        if related_projects.count() < 3:
            remaining_needed = 3 - related_projects.count()
            same_theme_projects = Project.objects.filter(
                theme=project.theme,
                is_active=True
            ).exclude(
                pk=project.pk,
                pk__in=[p.pk for p in related_projects]
            ).order_by('-created_at')[:remaining_needed]
            related_projects = list(related_projects) + list(same_theme_projects)
        
        # Priority 3: If still not enough results, get projects from same country
        if len(related_projects) < 3:
            remaining_needed = 3 - len(related_projects)
            same_country_projects = Project.objects.filter(
                country=project.country,
                is_active=True
            ).exclude(
                pk=project.pk,
                pk__in=[p.pk for p in related_projects]
            ).order_by('-created_at')[:remaining_needed]
            related_projects = list(related_projects) + list(same_country_projects)
        
        context['related_projects'] = related_projects[:3]
        
        return context

@login_required
def apply_to_project(request, pk):
    try:
        project = Project.objects.get(pk=pk, is_active=True)
    except Project.DoesNotExist:
        messages.error(request, _('Project not found.'))
        return redirect('content_project_list')
    
    if not project.can_user_apply(request.user):
        if project.is_full:
            messages.error(request, _('This project is already full.'))
        elif project.enrolled_users.filter(id=request.user.id).exists():
            messages.info(request, _('You are already enrolled in this project.'))
        else:
            messages.error(request, _('You cannot apply to this project.'))
        return redirect('content_project_detail', pk=pk)
    
    if request.method == 'POST':
        # Apply to project
        project.enrolled_users.add(request.user)
        project.headcount = (project.headcount or 0) + 1
        project.save()
        
        messages.success(request, _('Successfully applied to "{project_title}".').format(project_title=project.title))
        return redirect('content_project_detail', pk=pk)
    
    # GET request: show confirmation
    return render(request, 'content/project_apply_confirm.html', {'project': project})

# News/Event Views
class NewsEventListView(ListView):
    model = NewsEvent
    template_name = 'content/news_event_list.html'
    context_object_name = 'news_events'
    paginate_by = 9

    def get_queryset(self):
        queryset = NewsEvent.objects.filter(is_published=True)
        # Filtering
        content_type = self.request.GET.get('content_type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        # Searching
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        # Sorting
        sort = self.request.GET.get('sort', '-publish_date')
        queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import NewsEvent
        published_news_events = NewsEvent.objects.filter(is_published=True)
        # Get hero news/events for carousel
        context['hero_news_events'] = published_news_events.filter(is_hero_highlight=True).order_by('-publish_date')[:3]
        # Get featured news/events
        context['featured_news_events'] = published_news_events.filter(is_featured=True).order_by('-publish_date')[:3]
        context['content_types'] = NewsEvent.Type.choices
        context['sort_options'] = [
            {'value': '-publish_date', 'label': _('Publication Date (Newest First)')},
            {'value': 'publish_date', 'label': _('Publication Date (Oldest First)')},
            {'value': 'title', 'label': _('Title (A-Z)')},
            {'value': '-title', 'label': _('Title (Z-A)')},
        ]
        return context

class NewsEventDetailView(DetailView):
    model = NewsEvent
    template_name = 'content/news_event_detail.html'
    context_object_name = 'news_event'
    queryset = NewsEvent.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_event = self.object
        
        # Related news/events with smart filtering logic
        # Priority 1: Same content type (closest match)
        related_news_events = NewsEvent.objects.filter(
            content_type=news_event.content_type,
            is_published=True
        ).exclude(pk=news_event.pk).order_by('-publish_date')[:3]
        
        # Priority 2: If not enough results, get any published news/events (most recent)
        if related_news_events.count() < 3:
            remaining_needed = 3 - related_news_events.count()
            other_news_events = NewsEvent.objects.filter(
                is_published=True
            ).exclude(
                pk=news_event.pk,
                pk__in=[ne.pk for ne in related_news_events]
            ).order_by('-publish_date')[:remaining_needed]
            related_news_events = list(related_news_events) + list(other_news_events)
        
        context['related_news_events'] = related_news_events[:3]
        
        return context

# Success Story Views
class SuccessStoryListView(ListView):
    model = SuccessStory
    template_name = 'content/success_story_list.html'
    context_object_name = 'success_stories'
    paginate_by = 9

    def get_queryset(self):
        queryset = SuccessStory.objects.filter(is_published=True)
        # Filtering (by related_project if ID provided)
        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(related_project_id=project_id)
        # Searching
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        # Sorting
        sort = self.request.GET.get('sort', '-published_at')
        queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Project
        published_success_stories = SuccessStory.objects.filter(is_published=True)
        # Get hero success stories for carousel
        context['hero_success_stories'] = published_success_stories.filter(is_hero_highlight=True).order_by('-published_at')[:3]
        # Get featured success stories
        context['featured_success_stories'] = published_success_stories.filter(is_featured=True).order_by('-published_at')[:3]
        context['projects'] = Project.objects.filter(is_active=True).values('id', 'title')
        context['sort_options'] = [
            {'value': '-published_at', 'label': _('Publication Date (Newest First)')},
            {'value': 'published_at', 'label': _('Publication Date (Oldest First)')},
            {'value': 'title', 'label': _('Title (A-Z)')},
            {'value': '-title', 'label': _('Title (Z-A)')},
        ]
        return context

class SuccessStoryDetailView(DetailView):
    model = SuccessStory
    template_name = 'content/success_story_detail.html'
    context_object_name = 'success_story'
    queryset = SuccessStory.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_story = self.object
        
        # Related success stories with smart filtering logic
        related_stories = []
        
        # Priority 1: Stories from the same project (closest match)
        if success_story.related_project:
            related_stories = SuccessStory.objects.filter(
                related_project=success_story.related_project,
                is_published=True
            ).exclude(pk=success_story.pk).order_by('-published_at')[:3]
        
        # Priority 2: If not enough results and story has a project, get stories with same theme
        if len(related_stories) < 3 and success_story.related_project:
            remaining_needed = 3 - len(related_stories)
            same_theme_stories = SuccessStory.objects.filter(
                related_project__theme=success_story.related_project.theme,
                is_published=True
            ).exclude(
                pk=success_story.pk,
                pk__in=[s.pk for s in related_stories]
            ).order_by('-published_at')[:remaining_needed]
            related_stories = list(related_stories) + list(same_theme_stories)
        
        # Priority 3: If still not enough results, get any published stories (most recent)
        if len(related_stories) < 3:
            remaining_needed = 3 - len(related_stories)
            other_stories = SuccessStory.objects.filter(
                is_published=True
            ).exclude(
                pk=success_story.pk,
                pk__in=[s.pk for s in related_stories]
            ).order_by('-published_at')[:remaining_needed]
            related_stories = list(related_stories) + list(other_stories)
        
        context['related_success_stories'] = related_stories[:3]
        
        return context

# FAQ Views
class FAQListView(ListView):
    model = FAQ
    template_name = 'content/faq_list.html'
    context_object_name = 'faqs'
    paginate_by = 9

    def get_queryset(self):
        queryset = FAQ.objects.all()
        # Searching
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(question__icontains=search) |
                Q(answer__icontains=search)
            )
        # Sorting
        sort = self.request.GET.get('sort', 'order')
        queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_options'] = [
            {'value': 'order', 'label': _('Default Order')},
            {'value': 'question', 'label': _('Question (A-Z)')},
            {'value': '-question', 'label': _('Question (Z-A)')},
            {'value': 'created_at', 'label': _('Newest First')}
        ]
        return context

# Landing Page View
def landing_page_view(request):
    # Get hero highlighted items (is_hero_highlight)
    hero_projects = Project.objects.filter(is_active=True, is_hero_highlight=True).order_by('-created_at')[:3]
    hero_news_events = NewsEvent.objects.filter(is_published=True, is_hero_highlight=True).order_by('-publish_date')[:3]
    hero_success_stories = SuccessStory.objects.filter(is_published=True, is_hero_highlight=True).order_by('-published_at')[:3]
    
    # Get featured items first, then fall back to latest if no featured items exist
    featured_projects = Project.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:3]
    latest_projects = featured_projects if featured_projects.exists() else Project.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    featured_news_events = NewsEvent.objects.filter(is_published=True, is_featured=True).order_by('-publish_date')[:3]
    latest_news_events = featured_news_events if featured_news_events.exists() else NewsEvent.objects.filter(is_published=True).order_by('-publish_date')[:3]
    
    featured_success_stories = SuccessStory.objects.filter(is_published=True, is_featured=True).order_by('-published_at')[:3]
    latest_success_stories = featured_success_stories if featured_success_stories.exists() else SuccessStory.objects.filter(is_published=True).order_by('-published_at')[:3]
    
    latest_faqs = FAQ.objects.order_by('order')[:5]

    context = {
        'hero_projects': hero_projects,
        'hero_news_events': hero_news_events,
        'hero_success_stories': hero_success_stories,
        'latest_projects': latest_projects,
        'latest_news_events': latest_news_events,
        'latest_success_stories': latest_success_stories,
        'latest_faqs': latest_faqs,
    }
    return render(request, 'content/landing_page.html', context)


def serve_blob(request, model_name, pk, field_name):
    """Serve a binary blob field stored on a model.

    URL pattern: /content/blob/<model_name>/<pk>/<field_name>/
    model_name: 'project' | 'news_event' | 'success_story'
    field_name: the blob field name, e.g. 'cover_image_blob' or 'image_file_blob'
    """
    Model = _BLOB_MODEL_MAP.get(model_name)
    if Model is None:
        raise Http404("Unknown model")

    obj = get_object_or_404(Model, pk=pk)

    # Only allow a small whitelist of blob fields to be served
    allowed_fields = {
        Project: {'cover_image_blob',},
        NewsEvent: {'cover_image_blob',},
        SuccessStory: {'cover_image_blob', 'image_file_blob'},
    }

    if field_name not in allowed_fields.get(Model, set()):
        raise Http404("Field not allowed")

    blob = getattr(obj, field_name, None)
    if not blob:
        raise Http404("Blob not found")

    # try to get mime type from metadata field if present
    mime_field = field_name + '_mime'
    name_field = field_name.replace('_blob', '_name')
    content_type = getattr(obj, mime_field, None) or 'application/octet-stream'
    filename = getattr(obj, name_field, '') or ''

    resp = HttpResponse(blob, content_type=content_type)
    if filename:
        resp['Content-Disposition'] = f'inline; filename="{filename}"'
    return resp