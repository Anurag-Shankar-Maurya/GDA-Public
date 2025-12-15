from django import template
import re

register = template.Library()

@register.filter(name='embed_youtube')
def embed_youtube(url):
    """Converts a YouTube URL into an embeddable URL."""
    if not url:
        return ""

    # Check if already an embed URL
    if 'youtube.com/embed/' in url or 'youtube-nocookie.com/embed/' in url:
        return url

    # Extract video ID from various YouTube URL formats
    # Handles: https://www.youtube.com/watch?v=VIDEO_ID, https://youtu.be/VIDEO_ID, and https://www.youtube.com/shorts/VIDEO_ID
    
    # For youtu.be format
    if 'youtu.be/' in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1).split('?')[0].split('&')[0]
            # YouTube video IDs are always 11 characters, take only first 11
            if len(video_id) > 11:
                video_id = video_id[:11]
            # Use youtube-nocookie.com for better privacy and fewer restrictions
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
    
    # For youtube.com/watch format
    if 'youtube.com/watch' in url:
        match = re.search(r'[?&]v=([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1).split('&')[0]
            # YouTube video IDs are always 11 characters, take only first 11
            if len(video_id) > 11:
                video_id = video_id[:11]
            # Use youtube-nocookie.com for better privacy and fewer restrictions
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
    
    # For youtube.com/shorts format
    if 'youtube.com/shorts/' in url:
        match = re.search(r'shorts/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1).split('?')[0].split('&')[0]
            # YouTube video IDs are always 11 characters, take only first 11
            if len(video_id) > 11:
                video_id = video_id[:11]
            # Use youtube-nocookie.com for better privacy and fewer restrictions
            return f"https://www.youtube-nocookie.com/embed/{video_id}"

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
