from django import forms
from apps.content.models import Project, NewsEvent, SuccessStory, FAQ

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['title', 'teaser', 'background_objectives', 'tasks_eligibility', 'country', 'theme', 
                   'cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name', 'project_id']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'application_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NewsEventForm(forms.ModelForm):
    class Meta:
        model = NewsEvent
        exclude = ['title', 'body', 'news_event_id', 
                   'cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name']
        widgets = {
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SuccessStoryForm(forms.ModelForm):
    class Meta:
        model = SuccessStory
        exclude = ['title', 'body', 'success_story_id',
                   'cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name']
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        exclude = ['question', 'answer', 'faq_id']
