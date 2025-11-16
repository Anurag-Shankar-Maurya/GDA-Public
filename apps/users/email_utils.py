"""
Email utility module for sending HTML emails with fallback to plain text.
Provides helper functions for sending verification, password reset, and other transactional emails.
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_html_email(
    subject,
    recipient_list,
    template_name,
    context,
    plain_text_template=None,
    from_email=None,
    fail_silently=False,
    tags=None
):
    """
    Send an HTML email with optional plain text fallback.
    
    Args:
        subject (str): Email subject line
        recipient_list (list): List of recipient email addresses
        template_name (str): Path to HTML email template
        context (dict): Context dictionary for template rendering
        plain_text_template (str, optional): Path to plain text fallback template
        from_email (str, optional): Sender email address (defaults to DEFAULT_FROM_EMAIL)
        fail_silently (bool): Whether to suppress exceptions during sending
        tags (list, optional): Email tags for tracking (if using services like SendGrid)
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        
        # Validate email configuration
        if not from_email or from_email.strip() == '':
            error_msg = (
                "Email configuration error: DEFAULT_FROM_EMAIL is not set. "
                "Please configure EMAIL_HOST_USER environment variable or set DEFAULT_FROM_EMAIL."
            )
            logger.error(error_msg)
            if not fail_silently:
                raise ValueError(error_msg)
            return False, error_msg
        
        # Check if email authentication is configured (for Gmail/SMTP)
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            error_msg = (
                "Email configuration error: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set. "
                "Email functionality requires proper SMTP authentication credentials."
            )
            logger.error(error_msg)
            if not fail_silently:
                raise ValueError(error_msg)
            return False, error_msg
        
        if not recipient_list or not all(recipient_list):
            error_msg = "Invalid recipient list: must contain at least one valid email address"
            logger.error(error_msg)
            if not fail_silently:
                raise ValueError(error_msg)
            return False, error_msg
        
        # Render HTML content
        html_content = render_to_string(template_name, context)
        
        # Render plain text content if template provided
        text_content = None
        if plain_text_template:
            try:
                text_content = render_to_string(plain_text_template, context)
            except Exception as e:
                logger.warning(f"Failed to render plain text template {plain_text_template}: {str(e)}")
        
        # If no plain text template, extract basic text from HTML
        if not text_content:
            text_content = _extract_text_from_html(html_content)
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipient_list
        )
        
        # Attach HTML alternative
        msg.attach_alternative(html_content, "text/html")
        
        # Add tags if provided (for email services)
        if tags:
            msg.tags = tags
        
        # Send email
        msg.send(fail_silently=fail_silently)
        
        logger.info(f"HTML email '{subject}' sent successfully to {recipient_list}")
        return True, None
        
    except Exception as e:
        error_msg = f"Failed to send HTML email '{subject}' to {recipient_list}: {str(e)}"
        logger.error(error_msg)
        if not fail_silently:
            raise
        return False, str(e)


def _extract_text_from_html(html_content):
    """
    Extract plain text from HTML content for email fallback.
    This is a simple implementation that removes HTML tags.
    
    Args:
        html_content (str): HTML content
    
    Returns:
        str: Plain text version
    """
    import re
    
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', text)
    
    # Decode HTML entities
    import html
    text = html.unescape(text)
    
    # Clean up whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    return text


def send_verification_email(request, user):
    """
    Send HTML verification email to user.
    
    Args:
        request: Django request object (for building absolute URI)
        user: User object with email attribute
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.urls import reverse
    
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        verification_link = request.build_absolute_uri(
            reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        )
        
        context = {
            'user': user,
            'verification_link': verification_link,
        }
        
        return send_html_email(
            subject='Verify your email - GDA',
            recipient_list=[user.email],
            template_name='users/emails/verification_email.html',
            plain_text_template='users/emails/verification_email.txt',
            context=context,
            tags=['verification', 'transactional']
        )
        
    except Exception as e:
        error_msg = f"Error preparing verification email for {user.email}: {str(e)}"
        logger.error(error_msg)
        return False, str(e)


def send_password_reset_email(user, use_https=True, request=None, **kwargs):
    """
    Send HTML password reset email to user.
    
    Args:
        user: User object
        use_https (bool): Whether to use HTTPS in reset link
        request: Django request object (for building domain)
        **kwargs: Additional context variables
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.contrib.sites.shortcuts import get_current_site
    
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        if request:
            site = get_current_site(request)
            domain = site.domain
        else:
            domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'example.com'
        
        protocol = 'https' if use_https else 'http'
        
        context = {
            'user': user,
            'protocol': protocol,
            'domain': domain,
            'uid': uid,
            'token': token,
        }
        context.update(kwargs)
        
        return send_html_email(
            subject='Password Reset - GDA',
            recipient_list=[user.email],
            template_name='users/emails/password_reset_email.html',
            plain_text_template='users/emails/password_reset_email.txt',
            context=context,
            tags=['password-reset', 'transactional']
        )
        
    except Exception as e:
        error_msg = f"Error preparing password reset email for {user.email}: {str(e)}"
        logger.error(error_msg)
        return False, str(e)
