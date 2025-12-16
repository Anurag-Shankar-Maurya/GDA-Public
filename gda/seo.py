from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
import os

def sitemap_view(request):
    """
    Serve the correct sitemap based on the request host.
    This mimics the Nginx configuration for environments where Nginx is not present (e.g. Vercel).
    """
    host = request.get_host()
    filename = f'sitemap_{host}.xml'
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    filepath = os.path.join(static_dir, filename)
    
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='application/xml')
        
    # Fallback to sitemap.xml (Index)
    fallback_path = os.path.join(static_dir, 'sitemap.xml')
    if os.path.exists(fallback_path):
        return FileResponse(open(fallback_path, 'rb'), content_type='application/xml')
        
    raise Http404

def robots_view(request):
    """
    Serve robots.txt from static directory.
    """
    filepath = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='text/plain')
    raise Http404
