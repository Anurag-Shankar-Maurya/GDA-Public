from rest_framework import serializers
from .models import Project, NewsEvent, SuccessStory, FAQ

class ProjectSerializer(serializers.ModelSerializer):
    gallery_images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'project_id', 'kicc_project_id', 'title', 'teaser', 
                 'background_objectives', 'tasks_eligibility', 'country', 'theme',
                 'duration', 'difficulty', 'headcount', 'total_headcount', 
                 'cover_image', 'cover_image_url', 'video_urls', 'image_urls',
                 'gallery_images_count', 'application_deadline', 'start_date', 
                 'end_date', 'is_active', 'is_hero_highlight', 'is_featured',
                 'created_at', 'updated_at']
    
    def get_gallery_images_count(self, obj):
        """Return the count of gallery images"""
        return obj.gallery_images.count()

class NewsEventSerializer(serializers.ModelSerializer):
    gallery_images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsEvent
        fields = ['id', 'news_event_id', 'title', 'body', 'content_type',
                 'cover_image', 'cover_image_url', 'external_link', 
                 'video_urls', 'image_urls', 'gallery_images_count',
                 'publish_date', 'is_published', 'is_hero_highlight', 
                 'is_featured', 'created_at', 'updated_at']
    
    def get_gallery_images_count(self, obj):
        """Return the count of gallery images"""
        return obj.gallery_images.count()

class SuccessStorySerializer(serializers.ModelSerializer):
    gallery_images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SuccessStory
        fields = ['id', 'success_story_id', 'title', 'body', 
                 'related_project', 'cover_image', 'cover_image_url',
                 'is_hero_highlight', 'is_featured', 'image_urls', 'video_urls',
                 'gallery_images_count', 'beneficiaries', 'total_hours_contributed',
                 'is_published', 'published_at', 'created_at', 'updated_at']
    
    def get_gallery_images_count(self, obj):
        """Return the count of gallery images"""
        return obj.gallery_images.count()

class FAQSerializer(serializers.ModelSerializer):
    total_votes = serializers.ReadOnlyField()
    helpfulness_ratio = serializers.ReadOnlyField()
    
    class Meta:
        model = FAQ
        fields = ['id', 'faq_id', 'question', 'answer', 'order', 
                 'is_schema_ready', 'thumbs_up', 'thumbs_down', 
                 'total_votes', 'helpfulness_ratio', 'created_at', 'updated_at']