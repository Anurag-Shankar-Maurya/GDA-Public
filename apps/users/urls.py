from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import sync_views

urlpatterns = [
    # Use custom login view instead of allauth redirect
    path('login/', views.login_view, name='login'),
    # Custom registration view
    path('register/', views.register, name='register'),
    # Logout view
    path('logout/', views.logout_view, name='logout'),
    # Custom password reset view
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    
    # Keep custom profile and onboarding URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/accounts/', views.account_management, name='account_management'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('profile/certificates/generate/<int:project_id>/', views.generate_certificate, name='generate_certificate'),
    path('profile/certificates/view/<str:certificate_id>/', views.view_certificate, name='view_certificate'),
    path('onboarding/', views.onboarding, name='onboarding'),
    
    # Keep custom email verification URLs (used by custom email system)
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('verify-certificate/<str:certificate_id>', views.certificate_verification_url, name='certificate_verification_url'),
    
    # Sync API endpoints
    path('sync/create-user/', sync_views.sync_create_user, name='sync_create_user'),
    path('sync/check-user/', sync_views.sync_check_user, name='sync_check_user'),
    path('sync/health/', sync_views.sync_health_check, name='sync_health_check'),
]
