from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.ManagementDashboardView.as_view(), name='management_dashboard'),
    path('dashboard-data/', views.DashboardDataView.as_view(), name='dashboard_data'),
    path('user-analytics/', views.UserAnalyticsView.as_view(), name='user_analytics'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('application-analytics/', views.ApplicationAnalyticsView.as_view(), name='application_analytics'),

    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # News/Event URLs
    path('news-events/', views.NewsEventListView.as_view(), name='news_event_list'),
    path('news-events/create/', views.NewsEventCreateView.as_view(), name='news_event_create'),
    path('news-events/<int:pk>/', views.NewsEventDetailView.as_view(), name='news_event_detail'),
    path('news-events/<int:pk>/update/', views.NewsEventUpdateView.as_view(), name='news_event_update'),
    path('news-events/<int:pk>/delete/', views.NewsEventDeleteView.as_view(), name='news_event_delete'),

    # Success Story URLs
    path('success-stories/', views.SuccessStoryListView.as_view(), name='success_story_list'),
    path('success-stories/create/', views.SuccessStoryCreateView.as_view(), name='success_story_create'),
    path('success-stories/<int:pk>/', views.SuccessStoryDetailView.as_view(), name='success_story_detail'),
    path('success-stories/<int:pk>/update/', views.SuccessStoryUpdateView.as_view(), name='success_story_update'),
    path('success-stories/<int:pk>/delete/', views.SuccessStoryDeleteView.as_view(), name='success_story_delete'),

    # FAQ URLs
    path('faqs/', views.FAQListView.as_view(), name='faq_list'),
    path('faqs/create/', views.FAQCreateView.as_view(), name='faq_create'),
    path('faqs/<int:pk>/', views.FAQDetailView.as_view(), name='faq_detail'),
    path('faqs/<int:pk>/update/', views.FAQUpdateView.as_view(), name='faq_update'),
    path('faqs/<int:pk>/delete/', views.FAQDeleteView.as_view(), name='faq_delete'),

    # User URLs
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
]
