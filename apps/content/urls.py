from django.urls import path
from . import views

urlpatterns = [
    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='content_project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='content_project_detail'),
    path('projects/<int:pk>/apply/', views.apply_to_project, name='apply_to_project'),

    # News/Event URLs
    path('news-events/', views.NewsEventListView.as_view(), name='content_news_event_list'),
    path('news-events/<int:pk>/', views.NewsEventDetailView.as_view(), name='content_news_event_detail'),

    # Success Story URLs
    path('success-stories/', views.SuccessStoryListView.as_view(), name='content_success_story_list'),
    path('success-stories/<int:pk>/', views.SuccessStoryDetailView.as_view(), name='content_success_story_detail'),

    # FAQ URLs
    path('faq/', views.FAQListView.as_view(), name='content_faq_list'),
    path('', views.landing_page_view, name='landing_page'),
    # Blob access (serves images stored in model BinaryField)
    path('blob/<str:model_name>/<int:pk>/<str:field_name>/', views.serve_blob, name='content_serve_blob'),
]
