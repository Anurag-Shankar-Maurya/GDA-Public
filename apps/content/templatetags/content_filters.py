from django import template
import re

register = template.Library()

@register.filter(name='embed_youtube')
def embed_youtube(url):
    """Converts a YouTube URL into an embeddable URL."""
    if not url:
        return ""

    # Check if already an embed URL
    if 'youtube.com/embed/' in url:
        return url

    # Extract video ID from various YouTube URL formats
    # Handles: https://www.youtube.com/watch?v=VIDEO_ID, https://youtu.be/VIDEO_ID, and https://www.youtube.com/shorts/VIDEO_ID
    patterns = [
        r"(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"

    return url  # Return original URL if no match is found

@register.filter(name='google_drive_image_embed')
def google_drive_image_embed(url):
    """Converts a Google Drive image URL into a direct embeddable URL."""
    if not url:
        return ""
    match = re.search(r"file/d/([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        # Using the thumbnail service for more reliable direct image embedding
        return f"https://drive.google.com/thumbnail?id={file_id}"
    return url

@register.filter(name='google_drive_video_embed')
def google_drive_video_embed(url):
    """Converts a Google Drive video URL into an embeddable URL."""
    if not url:
        return ""
    match = re.search(r"file/d/([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"
    return url
