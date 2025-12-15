"""
URL configuration for gda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.content.api_views import ProjectViewSet, NewsEventViewSet, SuccessStoryViewSet, FAQViewSet
from apps.users.api_views import UserViewSet, CertificateViewSet, SocialAccountViewSet

from apps.users import views as user_views

# Create a router for REST API
router = routers.DefaultRouter()
router.register(r'api/projects', ProjectViewSet)
router.register(r'api/news-events', NewsEventViewSet)
router.register(r'api/success-stories', SuccessStoryViewSet)
router.register(r'api/users', UserViewSet)
router.register(r'api/certificates', CertificateViewSet)
router.register(r'api/social-accounts', SocialAccountViewSet, basename='socialaccount')
router.register(r'api/faq', FAQViewSet)

# Schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="GDA API",
        default_version='v1',
        description="API documentation for GDA",
        terms_of_service="/terms-of-service/",
        contact=openapi.Contact(email="anuragshankarmaurya@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.content.urls')),
    path('management/', include('apps.content_management.urls')),
    path('', include('apps.users.urls')),
    # Override allauth login with custom view
    path('accounts/login/', user_views.login_view, name='account_login'),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('health/', lambda r: HttpResponse('OK')),
    # API URLs
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # Swagger documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
