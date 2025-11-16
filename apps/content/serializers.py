from rest_framework import serializers
from .models import Project, NewsEvent, SuccessStory

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_id', 'kicc_project_id', 'title', 'teaser', 
                 'background_objectives', 'tasks_eligibility', 'country', 'theme',
                 'duration', 'difficulty', 'headcount', 'total_headcount', 
                 'cover_image', 'cover_image_url']

class NewsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsEvent
        fields = ['id', 'news_event_id', 'title', 'body', 'content_type',
                 'cover_image', 'cover_image_url', 'external_link', 
                 'publish_date', 'is_published', 'is_hero_highlight', 
                 'is_featured', 'created_at', 'updated_at']

class SuccessStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessStory
        fields = ['id', 'success_story_id', 'title', 'body', 
                 'related_project', 'cover_image', 'cover_image_url',
                 'is_hero_highlight', 'created_at', 'updated_at']