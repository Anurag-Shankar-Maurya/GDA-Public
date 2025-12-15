from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Project, NewsEvent, SuccessStory, SuccessStoryGalleryImage, ProjectGalleryImage, NewsEventGalleryImage, FAQ, FAQVote
import json
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

_BLOB_MODEL_MAP = {
    'project': Project,
    'news_event': NewsEvent,
    'success_story': SuccessStory,
    'success_story_gallery_image': SuccessStoryGalleryImage,
    'project_gallery_image': ProjectGalleryImage,
    'news_event_gallery_image': NewsEventGalleryImage,
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
        
        # Category filtering (Past, Current, Upcoming)
        category = self.request.GET.get('category')
        if category:
            from django.utils import timezone
            now = timezone.now().date()
            
            if category == 'past':
                # Projects that have ended
                queryset = queryset.filter(end_date__lt=now)
            elif category == 'current':
                # Projects that are currently running
                queryset = queryset.filter(
                    start_date__lte=now,
                    end_date__gte=now
                )
            elif category == 'upcoming':
                # Projects that haven't started yet
                queryset = queryset.filter(start_date__gt=now)
        
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
        context['categories'] = [
            {'value': 'past', 'label': _('Past')},
            {'value': 'current', 'label': _('Current')},
            {'value': 'upcoming', 'label': _('Upcoming')},
        ]
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
    queryset = Project.objects.filter(is_active=True).prefetch_related('gallery_images')

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
        
        # Related projects with smart filtering logic (always exclude current project)
        # Priority 1: Same theme AND same country (closest match)
        related_projects_qs = Project.objects.filter(
            theme=project.theme,
            country=project.country,
            is_active=True
        ).exclude(pk=project.pk).order_by('-created_at')

        # Start with queryset (no slicing yet)
        related_projects = list(related_projects_qs[:3])

        # Priority 2: If not enough results, get projects with same theme
        if len(related_projects) < 3:
            remaining_needed = 3 - len(related_projects)
            same_theme_qs = Project.objects.filter(
                theme=project.theme,
                is_active=True
            ).exclude(
                pk=project.pk
            ).exclude(pk__in=[p.pk for p in related_projects]).order_by('-created_at')[:remaining_needed]
            related_projects += list(same_theme_qs)

        # Priority 3: If still not enough results, get projects from same country
        if len(related_projects) < 3:
            remaining_needed = 3 - len(related_projects)
            same_country_qs = Project.objects.filter(
                country=project.country,
                is_active=True
            ).exclude(
                pk=project.pk
            ).exclude(pk__in=[p.pk for p in related_projects]).order_by('-created_at')[:remaining_needed]
            related_projects += list(same_country_qs)

        # Final safety: ensure current project is not included (dedupe by pk)
        deduped = []
        seen_pks = set()
        for p in related_projects:
            if p.pk == project.pk:
                continue
            if p.pk in seen_pks:
                continue
            seen_pks.add(p.pk)
            deduped.append(p)

        context['related_projects'] = deduped[:3]
        
        # Create unified gallery items list combining blob images, image URLs, and video URLs
        gallery_items = []
        
        # Add blob gallery images
        for idx, gallery_image in enumerate(project.gallery_images.all().order_by('order')):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': idx,
                'url': None,
                'caption': gallery_image.caption,
            })
        
        # Add image URLs
        blob_count = len(gallery_items)
        for idx, image_url in enumerate(project.image_urls):
            gallery_items.append({
                'type': 'image_url',
                'object': None,
                'index': blob_count + idx,
                'url': image_url,
                'caption': None,
            })
        
        # Add video URLs
        video_start_idx = len(gallery_items)
        for idx, video_url in enumerate(project.video_urls):
            gallery_items.append({
                'type': 'video_url',
                'object': None,
                'index': video_start_idx + idx,
                'url': video_url,
                'caption': None,
            })
        
        # Paginate the combined gallery items
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
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
        context['featured_news_events'] = published_news_events.filter(is_featured=True).order_by('-publish_date')[:4]
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
    queryset = NewsEvent.objects.filter(is_published=True).prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_event = self.object
        
        # Related news/events with smart filtering logic (always exclude current item)
        # Priority 1: Same content type (closest match)
        related_news_qs = NewsEvent.objects.filter(
            content_type=news_event.content_type,
            is_published=True
        ).exclude(pk=news_event.pk).order_by('-publish_date')

        related_news_events = list(related_news_qs[:3])

        # Priority 2: If not enough results, get any published news/events (most recent)
        if len(related_news_events) < 3:
            remaining_needed = 3 - len(related_news_events)
            other_news_qs = NewsEvent.objects.filter(
                is_published=True
            ).exclude(pk=news_event.pk).exclude(pk__in=[ne.pk for ne in related_news_events]).order_by('-publish_date')[:remaining_needed]
            related_news_events += list(other_news_qs)

        # Final safety: dedupe and ensure current is not present
        deduped_news = []
        seen_pks = set()
        for ne in related_news_events:
            if ne.pk == news_event.pk:
                continue
            if ne.pk in seen_pks:
                continue
            seen_pks.add(ne.pk)
            deduped_news.append(ne)

        context['related_news_events'] = deduped_news[:3]
        
        # Create unified gallery items list combining blob images, image URLs, and video URLs
        gallery_items = []
        
        # Add blob gallery images
        for idx, gallery_image in enumerate(news_event.gallery_images.all().order_by('order')):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': idx,
                'url': None,
                'caption': gallery_image.caption,
            })
        
        # Add image URLs
        blob_count = len(gallery_items)
        for idx, image_url in enumerate(news_event.image_urls):
            gallery_items.append({
                'type': 'image_url',
                'object': None,
                'index': blob_count + idx,
                'url': image_url,
                'caption': None,
            })
        
        # Add video URLs
        video_start_idx = len(gallery_items)
        for idx, video_url in enumerate(news_event.video_urls):
            gallery_items.append({
                'type': 'video_url',
                'object': None,
                'index': video_start_idx + idx,
                'url': video_url,
                'caption': None,
            })
        
        # Paginate the combined gallery items
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
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
    queryset = SuccessStory.objects.filter(is_published=True).prefetch_related('gallery_images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_story = self.object
        
        # Related success stories with smart filtering logic (always exclude current item)
        related_stories = []

        # Priority 1: Stories from the same project (closest match)
        if success_story.related_project:
            related_qs = SuccessStory.objects.filter(
                related_project=success_story.related_project,
                is_published=True
            ).exclude(pk=success_story.pk).order_by('-published_at')
            related_stories = list(related_qs[:3])

        # Priority 2: If not enough results and story has a project, get stories with same theme
        if len(related_stories) < 3 and success_story.related_project:
            remaining_needed = 3 - len(related_stories)
            same_theme_qs = SuccessStory.objects.filter(
                related_project__theme=success_story.related_project.theme,
                is_published=True
            ).exclude(pk=success_story.pk).exclude(pk__in=[s.pk for s in related_stories]).order_by('-published_at')[:remaining_needed]
            related_stories += list(same_theme_qs)

        # Priority 3: If still not enough results, get any published stories (most recent)
        if len(related_stories) < 3:
            remaining_needed = 3 - len(related_stories)
            other_qs = SuccessStory.objects.filter(is_published=True).exclude(pk=success_story.pk).exclude(pk__in=[s.pk for s in related_stories]).order_by('-published_at')[:remaining_needed]
            related_stories += list(other_qs)

        # Final safety: dedupe and ensure current not included
        deduped = []
        seen_pks = set()
        for s in related_stories:
            if s.pk == success_story.pk:
                continue
            if s.pk in seen_pks:
                continue
            seen_pks.add(s.pk)
            deduped.append(s)

        context['related_success_stories'] = deduped[:3]
        
        # Create unified gallery items list combining blob images, image URLs, and video URLs
        gallery_items = []
        
        # Add blob gallery images
        for idx, gallery_image in enumerate(success_story.gallery_images.all().order_by('order')):
            gallery_items.append({
                'type': 'blob_image',
                'object': gallery_image,
                'index': idx,
                'url': None,
                'caption': gallery_image.caption,
            })
        
        # Add image URLs
        blob_count = len(gallery_items)
        for idx, image_url in enumerate(success_story.image_urls):
            gallery_items.append({
                'type': 'image_url',
                'object': None,
                'index': blob_count + idx,
                'url': image_url,
                'caption': None,
            })
        
        # Add video URLs
        video_start_idx = len(gallery_items)
        for idx, video_url in enumerate(success_story.video_urls):
            gallery_items.append({
                'type': 'video_url',
                'object': None,
                'index': video_start_idx + idx,
                'url': video_url,
                'caption': None,
            })
        
        # Paginate the combined gallery items
        gallery_paginator = Paginator(gallery_items, 12)  # Show 20 items per page
        gallery_page_number = self.request.GET.get('gallery_page', 1)
        try:
            gallery_page_obj = gallery_paginator.page(gallery_page_number)
        except:
            gallery_page_obj = gallery_paginator.page(1)
        
        context['gallery_items'] = gallery_page_obj
        context['gallery_paginator'] = gallery_paginator
        
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
        # Add user votes for each FAQ
        if self.request.user.is_authenticated:
            user_faq_votes = {vote.faq_id: vote.vote_type for vote in FAQVote.objects.filter(user=self.request.user, faq__in=context['faqs'])}
            for faq in context['faqs']:
                faq.user_vote = user_faq_votes.get(faq.id, None)
        else:
            for faq in context['faqs']:
                faq.user_vote = None
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
    
    featured_news_events = NewsEvent.objects.filter(is_published=True, is_featured=True).order_by('-publish_date')[:4]
    latest_news_events = featured_news_events if featured_news_events.exists() else NewsEvent.objects.filter(is_published=True).order_by('-publish_date')[:4]
    
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


def about_view(request):
    """Render the static About page with founder and contact information."""
    # Minimal context - template contains mostly static content but keeping place for translations
    context = {
        'founder_name': 'Chen Qingyu',
        'contact_email': 'globaldevotion2017@gmail.com',
    }
    return render(request, 'content/founder.html', context)


def organization_view(request):
    """Render the Organization / Association page.

    This renders a mostly static page with the organization's structure,
    honorary members, contact details and other descriptive content.
    """
    # Minimal context for template; most content is static in the template itself
    context = {
        'page_title': 'About the Association',
        'contact_email': 'globaldevotion2017@gmail.com',
    }
    return render(request, 'content/organization.html', context)


def taiwan_cultural_experience_view(request):
    """Render the Taiwan Cultural Experience static page."""
    # Minimal context - template is mostly static and uses static images
    # Provide placeholders for up to 5 YouTube video IDs. Replace with real IDs or leave empty to show images.
    context = {
        'page_title': 'Taiwan Cultural Experience',
        'youtube_ids': ['', '', '', '', ''],
    }
    return render(request, 'content/taiwan_cultural_experience.html', context)


def amazing_taiwan_view(request):
    """Render the Amazing Taiwan static page."""
    context = {
        'page_title': 'Amazing Taiwan',
    }
    return render(request, 'content/amazing_taiwan.html', context)


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
        SuccessStory: {'cover_image_blob',},
        SuccessStoryGalleryImage: {'image_blob',},
        ProjectGalleryImage: {'image_blob',},
        NewsEventGalleryImage: {'image_blob',},
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

def privacy_policy_view(request):
    """Render the Privacy Policy static page."""
    return render(request, 'content/privacy_policy.html')

def taiwan_view(request):
    """Render the consolidated Taiwan page with both regions and cultural experiences."""
    return render(request, 'content/taiwan.html')

def terms_of_service_view(request):
    """Render the Terms of Service static page."""
    return render(request, 'content/terms_of_service.html')

def cookies_policy_view(request):
    """Render the Cookies Policy static page."""
    return render(request, 'content/cookies_policy.html')

def earth_day_view(request):
    """Render the Earth Day static page."""
    return render(request, 'content/earth_day.html')

def volunteer_video_upload_view(request):
    """Render the Volunteer Video Upload page."""
    return render(request, 'content/volunteer_video_upload.html')

def life_of_gong_school_view(request):
    """Render the Gong School Article List page."""
    return render(request, 'content/life_of_gong_school.html')

def green_declaration_2018_view(request):
    """Render the Green Declaration 2018 static page."""
    return render(request, 'content/green_declaration_2018.html')


@login_required
def vote_faq(request, faq_id):
    if request.method == 'POST':
        faq = get_object_or_404(FAQ, pk=faq_id)
        vote_type = request.POST.get('vote_type')
        if vote_type not in ['up', 'down']:
            return HttpResponse('Invalid vote type', status=400)
        
        vote_type_db = 'UP' if vote_type == 'up' else 'DOWN'
        
        # Check if user already voted
        existing_vote = FAQVote.objects.filter(user=request.user, faq=faq).first()
        if existing_vote:
            if existing_vote.vote_type == vote_type_db:
                # Already voted the same, remove vote (toggle off)
                existing_vote.delete()
                if vote_type_db == 'UP':
                    faq.thumbs_up = max(0, faq.thumbs_up - 1)
                else:
                    faq.thumbs_down = max(0, faq.thumbs_down - 1)
                faq.save()
                return HttpResponse('OK')
            else:
                # Change vote
                old_vote = existing_vote.vote_type
                existing_vote.vote_type = vote_type_db
                existing_vote.save()
                # Update counters
                if old_vote == 'UP':
                    faq.thumbs_up -= 1
                else:
                    faq.thumbs_down -= 1
                if vote_type_db == 'UP':
                    faq.thumbs_up += 1
                else:
                    faq.thumbs_down += 1
                faq.save()
        else:
            # New vote
            FAQVote.objects.create(user=request.user, faq=faq, vote_type=vote_type_db)
            if vote_type_db == 'UP':
                faq.thumbs_up += 1
            else:
                faq.thumbs_down += 1
            faq.save()
        
        return HttpResponse('OK')
    return HttpResponse('Invalid request', status=400)
