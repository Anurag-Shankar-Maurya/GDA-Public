from rest_framework import viewsets
from .models import Project, NewsEvent, SuccessStory, FAQ
from .serializers import ProjectSerializer, NewsEventSerializer, SuccessStorySerializer, FAQSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Projects
    """
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

class NewsEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for News & Events
    """
    queryset = NewsEvent.objects.all().order_by('-publish_date')
    serializer_class = NewsEventSerializer

class SuccessStoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Success Stories
    """
    queryset = SuccessStory.objects.all().order_by('-published_at')
    serializer_class = SuccessStorySerializer

class FAQViewSet(viewsets.ModelViewSet):
    """
    API endpoint for FAQs
    """
    queryset = FAQ.objects.all().order_by('order')
    serializer_class = FAQSerializer