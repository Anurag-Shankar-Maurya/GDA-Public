from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import mimetypes
import os

# -----------------------------------------------------------------------------
# 1. Project Model (CMS - FR-3.1)
# -----------------------------------------------------------------------------

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.CharField(
        max_length=32, 
        unique=True, 
        editable=False,
        blank=True,
        default=''
    )
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Generate project_id only for new instances without one
        if is_new and not self.project_id:
            self.project_id = f"project_id_{self.id}"
            # Update without triggering save again
            Project.objects.filter(pk=self.pk).update(project_id=self.project_id)
            # Update the instance attribute
            self.refresh_from_db(fields=['project_id'])

        # Copy uploaded cover_image bytes into the blob fields (if present).
        try:
            if self.cover_image and hasattr(self.cover_image, 'path'):
                with open(self.cover_image.path, 'rb') as f:
                    data = f.read()
                mime, _ = mimetypes.guess_type(self.cover_image.name)
                name = os.path.basename(self.cover_image.name)
                Project.objects.filter(pk=self.pk).update(
                    cover_image_blob=data,
                    cover_image_blob_mime=(mime or ''),
                    cover_image_blob_name=name,
                )
                self.refresh_from_db(fields=['cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name'])
        except Exception:
            # Don't break saves if blob copy fails
            pass
    """
    Core content model for volunteer opportunities.
    Translation fields (en, zh_tw) are handled by apps/content/translation.py via django-modeltranslation.
    """
    kicc_project_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text=_("The ID of the project in the External Service API (KICC).")
    )
    title = models.CharField(max_length=255)
    teaser = models.TextField()
    background_objectives = models.TextField()
    tasks_eligibility = models.TextField()
    
    # Metadata for Filters/Cards
    country = models.CharField(max_length=100, db_index=True)
    theme = models.CharField(
        max_length=100, 
        db_index=True, 
        help_text=_("Hot categories (e.g., Education, Medical).")
    )
    duration = models.IntegerField(
        db_index=True, 
        help_text=_("Estimated total hours.")
    )
    difficulty = models.CharField(
        max_length=50, 
        db_index=True, 
        choices=[('Easy', _('Easy')), ('Medium', _('Medium')), ('Hard', _('Hard'))],
        help_text=_("Difficulty level of the project.")
    )
    headcount = models.IntegerField(
        default=0, 
        null=True, 
        blank=True, 
        help_text=_("Current number of volunteers signed up.")
    )
    total_headcount = models.IntegerField(
        default=0, 
        help_text=_("Maximum allowed headcount for the project.")
    )
    cover_image = models.ImageField(
        upload_to='project_covers/', 
        null=True, 
        blank=True
    )
    # Blob storage of the uploaded image for environments that prefer DB blobs
    cover_image_blob = models.BinaryField(null=True, blank=True, editable=False)
    cover_image_blob_mime = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_blob_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_url = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        help_text=_("Or provide a URL for the cover image.")
    )
    
    # Media Fields - Video URLs support
    video_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of video URLs (YouTube, Vimeo, etc.) for the media gallery.")
    )
    image_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of image URLs for the media gallery.")
    )
    
    # Scheduling & Status
    application_deadline = models.DateTimeField(db_index=True)
    start_date = models.DateField(null=True, blank=True, help_text=_("Project start date"))
    end_date = models.DateField(null=True, blank=True, help_text=_("Project end date"))
    is_active = models.BooleanField(default=True)
    is_hero_highlight = models.BooleanField(
        default=False, 
        help_text=_("For Hero Carousel (FR-1.2).")
    )
    is_featured = models.BooleanField(
        default=False,
        help_text=_("Featured projects appear in prominent positions across the site.")
    )
    
    # Enrolled users
    enrolled_users = models.ManyToManyField('users.CustomUser', blank=True, related_name='enrolled_projects')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        return (self.headcount or 0) >= self.total_headcount

    def can_user_apply(self, user):
        if not user or not user.is_authenticated:
            return False
        if self.is_full:
            return False
        if self.enrolled_users.filter(id=user.id).exists():
            return False
        return True


# -----------------------------------------------------------------------------
# 2. News/Event Model (For 'News & Stories feed' component)
# -----------------------------------------------------------------------------

class NewsEvent(models.Model):
    id = models.AutoField(primary_key=True)
    news_event_id = models.CharField(
        max_length=32, 
        unique=True, 
        editable=False,
        blank=True,
        default=''
    )
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Generate news_event_id only for new instances without one
        if is_new and not self.news_event_id:
            self.news_event_id = f"news_event_id_{self.id}"
            # Update without triggering save again
            NewsEvent.objects.filter(pk=self.pk).update(news_event_id=self.news_event_id)
            # Update the instance attribute
            self.refresh_from_db(fields=['news_event_id'])

        # Copy uploaded cover_image bytes into the blob fields (if present).
        try:
            if self.cover_image and hasattr(self.cover_image, 'path'):
                with open(self.cover_image.path, 'rb') as f:
                    data = f.read()
                mime, _ = mimetypes.guess_type(self.cover_image.name)
                name = os.path.basename(self.cover_image.name)
                NewsEvent.objects.filter(pk=self.pk).update(
                    cover_image_blob=data,
                    cover_image_blob_mime=(mime or ''),
                    cover_image_blob_name=name,
                )
                self.refresh_from_db(fields=['cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name'])
        except Exception:
            pass

    """
    Model for general news, announcements, and events (as distinct from success stories).
    Covers the 'News & Stories feed' requirement (5.2) for non-success content.
    Translation fields handled by apps/content/translation.py.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    # Content type to categorize in the feed
    class Type(models.TextChoices):
        NEWS = 'NEWS', _('News')
        EVENT = 'EVENT', _('Event Announcement')
        ANNOUNCEMENT = 'ANNOUNCEMENT', _('General Announcement')
    
    content_type = models.CharField(
        max_length=50, 
        db_index=True, 
        choices=Type.choices, 
        default=Type.NEWS
    )
    
    cover_image = models.ImageField(
        upload_to='news_event_covers/', 
        null=True, 
        blank=True
    )
    cover_image_blob = models.BinaryField(null=True, blank=True, editable=False)
    cover_image_blob_mime = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_blob_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_url = models.URLField(
        max_length=500, 
        blank=True, 
        help_text=_("Or provide a URL for the cover image.")
    )
    external_link = models.URLField(
        max_length=500, 
        blank=True, 
        help_text=_("Optional link if the news is hosted elsewhere.")
    )
    
    # Media Fields - Video URLs support
    video_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of video URLs (YouTube, Vimeo, etc.) for the media gallery.")
    )
    image_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of image URLs for the media gallery.")
    )
    
    # Publication fields
    publish_date = models.DateTimeField(db_index=True, default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_hero_highlight = models.BooleanField(
        default=False, 
        help_text=_("For Hero Carousel display.")
    )
    is_featured = models.BooleanField(
        default=False,
        help_text=_("Featured news/events appear in prominent positions across the site.")
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("News/Event")
        verbose_name_plural = _("News & Events")
        ordering = ['-publish_date']
        
    def __str__(self):
        return f"[{self.get_content_type_display()}] {self.title}"


# -----------------------------------------------------------------------------
# 3. Success Story Model (Allows linking to a Project)
# -----------------------------------------------------------------------------

class SuccessStory(models.Model):
    id = models.AutoField(primary_key=True)
    success_story_id = models.CharField(
        max_length=32, 
        unique=True, 
        editable=False,
        blank=True,
        default=''
    )
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Generate success_story_id only for new instances without one
        if is_new and not self.success_story_id:
            self.success_story_id = f"success_story_id_{self.id}"
            # Update without triggering save again
            SuccessStory.objects.filter(pk=self.pk).update(success_story_id=self.success_story_id)
            # Update the instance attribute
            self.refresh_from_db(fields=['success_story_id'])

        # Copy uploaded cover_image and image_file bytes into blob fields (if present).
        try:
            if self.cover_image and hasattr(self.cover_image, 'path'):
                with open(self.cover_image.path, 'rb') as f:
                    data = f.read()
                mime, _ = mimetypes.guess_type(self.cover_image.name)
                name = os.path.basename(self.cover_image.name)
                SuccessStory.objects.filter(pk=self.pk).update(
                    cover_image_blob=data,
                    cover_image_blob_mime=(mime or ''),
                    cover_image_blob_name=name,
                )
                self.refresh_from_db(fields=['cover_image_blob', 'cover_image_blob_mime', 'cover_image_blob_name'])
        except Exception:
            pass



    """Model for video/text stories (5.6)."""
    title = models.CharField(max_length=255)
    body = models.TextField()
    
    # UX Improvement: Link the story back to the project it relates to for context
    related_project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='success_stories',
        help_text=_("The volunteer project this story is about.")
    )
    
    cover_image = models.ImageField(
        upload_to='success_story_covers/', 
        null=True, 
        blank=True
    )
    cover_image_blob = models.BinaryField(null=True, blank=True, editable=False)
    cover_image_blob_mime = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_blob_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    cover_image_url = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        help_text=_("Or provide a URL for the cover image.")
    )
    
    is_hero_highlight = models.BooleanField(
        default=False, 
        help_text=_("For Hero Carousel display.")
    )
    is_featured = models.BooleanField(
        default=False,
        help_text=_("Featured success stories appear in prominent positions across the site.")
    )
    
    # Media Fields - Multiple images and videos support
    # Note: Gallery images are now stored in the SuccessStoryGalleryImage model
    image_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of image URLs for the media gallery.")
    )
    video_urls = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_("List of video URLs for the media gallery.")
    )
    
    # Impact Metrics
    beneficiaries = models.IntegerField(null=True, blank=True)
    total_hours_contributed = models.IntegerField(null=True, blank=True)
    
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(db_index=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Success Story")
        verbose_name_plural = _("Success Stories")
        ordering = ['-published_at']

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# 4. Success Story Gallery Image Model (For multiple gallery images as blobs)
# -----------------------------------------------------------------------------

class SuccessStoryGalleryImage(models.Model):
    """Model to store multiple gallery images for a success story as blobs."""
    id = models.AutoField(primary_key=True)
    success_story = models.ForeignKey(
        SuccessStory,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        help_text=_("The success story this image belongs to.")
    )
    
    # Blob storage for the uploaded image
    image_blob = models.BinaryField(help_text=_("Image data stored as binary."))
    image_blob_mime = models.CharField(
        max_length=255,
        help_text=_("MIME type of the image (e.g., image/jpeg, image/png).")
    )
    image_blob_name = models.CharField(
        max_length=255,
        help_text=_("Original filename of the uploaded image.")
    )
    
    # Optional caption/description for the image
    caption = models.CharField(
        max_length=500,
        blank=True,
        help_text=_("Optional caption or description for this image.")
    )
    
    # Ordering field
    order = models.IntegerField(
        default=0,
        help_text=_("Display order for the gallery images.")
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Success Story Gallery Image")
        verbose_name_plural = _("Success Story Gallery Images")
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.success_story.title} - {self.image_blob_name}"


# -----------------------------------------------------------------------------
# 4.1. Project Gallery Image Model (For multiple gallery images as blobs)
# -----------------------------------------------------------------------------

class ProjectGalleryImage(models.Model):
    """Model to store multiple gallery images for a project as blobs."""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        help_text=_("The project this image belongs to.")
    )
    
    # Blob storage for the uploaded image
    image_blob = models.BinaryField(help_text=_("Image data stored as binary."))
    image_blob_mime = models.CharField(
        max_length=255,
        help_text=_("MIME type of the image (e.g., image/jpeg, image/png).")
    )
    image_blob_name = models.CharField(
        max_length=255,
        help_text=_("Original filename of the uploaded image.")
    )
    
    # Optional caption/description for the image
    caption = models.CharField(
        max_length=500,
        blank=True,
        help_text=_("Optional caption or description for this image.")
    )
    
    # Ordering field
    order = models.IntegerField(
        default=0,
        help_text=_("Display order for the gallery images.")
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Project Gallery Image")
        verbose_name_plural = _("Project Gallery Images")
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.image_blob_name}"


# -----------------------------------------------------------------------------
# 4.2. News Event Gallery Image Model (For multiple gallery images as blobs)
# -----------------------------------------------------------------------------

class NewsEventGalleryImage(models.Model):
    """Model to store multiple gallery images for a news/event as blobs."""
    id = models.AutoField(primary_key=True)
    news_event = models.ForeignKey(
        NewsEvent,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        help_text=_("The news/event this image belongs to.")
    )
    
    # Blob storage for the uploaded image
    image_blob = models.BinaryField(help_text=_("Image data stored as binary."))
    image_blob_mime = models.CharField(
        max_length=255,
        help_text=_("MIME type of the image (e.g., image/jpeg, image/png).")
    )
    image_blob_name = models.CharField(
        max_length=255,
        help_text=_("Original filename of the uploaded image.")
    )
    
    # Optional caption/description for the image
    caption = models.CharField(
        max_length=500,
        blank=True,
        help_text=_("Optional caption or description for this image.")
    )
    
    # Ordering field
    order = models.IntegerField(
        default=0,
        help_text=_("Display order for the gallery images.")
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("News/Event Gallery Image")
        verbose_name_plural = _("News/Event Gallery Images")
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.news_event.title} - {self.image_blob_name}"


# -----------------------------------------------------------------------------
# 5. FAQ Model
# -----------------------------------------------------------------------------

class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    faq_id = models.CharField(
        max_length=32, 
        unique=True, 
        editable=False,
        blank=True,
        default=''
    )
    
    def save(self, *args, **kwargs):
        # Check if this is a new instance
        is_new = self.pk is None
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Generate faq_id only for new instances without one
        if is_new and not self.faq_id:
            self.faq_id = f"faq_id_{self.id}"
            # Update without triggering save again
            FAQ.objects.filter(pk=self.pk).update(faq_id=self.faq_id)
            # Update the instance attribute
            self.refresh_from_db(fields=['faq_id'])

    """Model for the Searchable FAQ section (5.7)."""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(db_index=True, default=0, unique=True)
    
    # Required for SEO Schema Markup (NFR-C3)
    is_schema_ready = models.BooleanField(default=True)
    
    # User feedback tracking
    thumbs_up = models.PositiveIntegerField(default=0, help_text=_("Number of thumbs up votes"), blank=True)
    thumbs_down = models.PositiveIntegerField(default=0, help_text=_("Number of thumbs down votes"), blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_votes(self):
        """Total number of votes cast."""
        return self.thumbs_up + self.thumbs_down

    @property
    def helpfulness_ratio(self):
        """Ratio of helpful votes (thumbs_up / total_votes). Returns 0 if no votes."""
        if self.total_votes == 0:
            return 0
        return round((self.thumbs_up / self.total_votes) * 100, 1)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['order'] 
    
    def __str__(self):
        return self.question[:50]


# ----------------------------------------------------------------------------- 
# 6. FAQ Vote Model
# -----------------------------------------------------------------------------

class FAQVote(models.Model):
    """Model to track individual user votes on FAQs."""
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='faq_votes')
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='votes')
    
    class VoteType(models.TextChoices):
        UP = 'UP', _('Thumbs Up')
        DOWN = 'DOWN', _('Thumbs Down')
    
    vote_type = models.CharField(
        max_length=4,
        choices=VoteType.choices,
        help_text=_("Type of vote: up or down.")
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = _("FAQ Vote")
        verbose_name_plural = _("FAQ Votes")
        unique_together = ('user', 'faq')  # One vote per user per FAQ
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.faq.question[:30]} - {self.get_vote_type_display()}"
