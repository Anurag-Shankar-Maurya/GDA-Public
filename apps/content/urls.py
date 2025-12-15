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
    path('faq/<int:faq_id>/vote/', views.vote_faq, name='vote_faq'),
    path('', views.landing_page_view, name='landing_page'),

    # Blob access (serves images stored in model BinaryField)
    path('blob/<str:model_name>/<int:pk>/<str:field_name>/', views.serve_blob, name='content_serve_blob'),

# -------------------- Additional Pages ---------------- #

    # Taiwan consolidated page
    path('taiwan/', views.taiwan_view, name='taiwan'),
    # Taiwan Cultural Experience page
    path('taiwan-cultural-experience/', views.taiwan_cultural_experience_view, name='taiwan_cultural_experience'),
    path('amazing-taiwan/', views.amazing_taiwan_view, name='amazing_taiwan'),

    # Organization information page
    path('organization/', views.organization_view, name='content_organization'),
    path('about/', views.about_view, name='founder'),

    # Privacy Policy page
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),

    # Cookies Policy page
    path('cookies-policy/', views.cookies_policy_view, name='cookies_policy'),

    # Terms of Service page
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),

    # Earth Day page
    path('earth-day/', views.earth_day_view, name='earth_day'),
    # Green Declaration 2018 page
    path('green-declaration-2018/', views.green_declaration_2018_view, name='green_declaration_2018'),
    # Volunteer Video Upload page
    path('volunteer-video-upload/', views.volunteer_video_upload_view, name='volunteer_video_upload'),
    # Gong School Article List page
    path('life-of-gong-school/', views.life_of_gong_school_view, name='life_of_gong_school'),
]
