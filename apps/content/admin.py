from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.db.models import Count, Q, F, Sum, Avg
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
import csv
import json
import base64
from .models import Project, NewsEvent, SuccessStory, SuccessStoryGalleryImage, ProjectGalleryImage, NewsEventGalleryImage, FAQ, FAQVote


class ExportMixin:
    """Mixin to add export functionality to admin classes"""
    
    def export_as_csv(self, request, queryset):
        """Export selected items as CSV"""
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        
        writer = csv.writer(response)
        writer.writerow(field_names)
        
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = '📥 Export selected as CSV'


class FAQVoteInline(admin.TabularInline):
    """Inline admin for viewing FAQ votes within FAQ admin"""
    model = FAQVote
    extra = 0
    readonly_fields = ('user', 'vote_type', 'created_at')
    fields = ('user', 'vote_type', 'created_at')
    ordering = ('-created_at',)
    can_delete = False
    show_change_link = False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


class ProjectGalleryImageInline(admin.TabularInline):
    """Inline admin for managing gallery images within Project admin"""
    model = ProjectGalleryImage
    extra = 1
    fields = ('image_preview', 'caption', 'order')
    readonly_fields = ('image_preview',)
    ordering = ['order']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image / Not Saved Yet"
    image_preview.short_description = 'Preview'


@admin.register(Project)
class ProjectAdmin(ExportMixin, TranslationAdmin):
    list_display = (
        'image_preview',
        'project_id', 
        'kicc_project_id', 
        'title', 
        'country', 
        'theme', 
        'difficulty',
        'headcount_display',
        'enrolled_count',
        'duration_display',
        'status_display',
        'is_active', 
        'is_hero_highlight',
        'is_featured',
        'start_date',
        'end_date',
        'application_deadline',
        'created_at'
    )
    
    readonly_fields = (
        'project_id', 
        'updated_at',
        'enrolled_users_display',
        'success_stories_display',
        'cover_image_blob',
        'cover_image_blob_mime',
        'cover_image_blob_name',
        'cover_image_preview'
    )
    
    list_filter = (
        'country', 
        'theme', 
        'is_active', 
        'is_hero_highlight', 
        'is_featured', 
        'difficulty',
        ('start_date', admin.DateFieldListFilter),
        ('end_date', admin.DateFieldListFilter),
        ('application_deadline', admin.DateFieldListFilter),
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = ('title', 'kicc_project_id', 'country', 'project_id', 'teaser', 'background_objectives', 'enrolled_users__username', 'enrolled_users__email')
    ordering = ('-created_at',)
    
    list_per_page = 50
    date_hierarchy = 'created_at'
    save_on_top = True
    
    # Editable fields directly in list view
    list_editable = ('is_active', 'is_hero_highlight', 'is_featured')
    
    # Enable actions
    actions = [
        'export_as_csv',
        'mark_as_active',
        'mark_as_inactive',
        'set_as_hero_highlight',
        'remove_hero_highlight',
        'set_as_featured',
        'remove_featured',
        'duplicate_project'
    ]
    
    # Autocomplete for enrolled users
    autocomplete_fields = ['enrolled_users']
    
    inlines = [ProjectGalleryImageInline]
    
    fieldsets = (
        ('Identification', {
            'fields': ('project_id', 'kicc_project_id'),
            'description': 'Unique identifiers for this project'
        }),
        ('Content', {
            'fields': ('title', 'teaser', 'background_objectives', 'tasks_eligibility'),
            'description': 'Main content and description of the project'
        }),
        ('Categorization', {
            'fields': ('country', 'theme', 'difficulty'),
            'description': 'Classification and filtering attributes'
        }),
        ('Capacity & Duration', {
            'fields': ('duration', 'headcount', 'total_headcount'),
            'description': 'Project capacity and duration settings'
        }),
        ('Enrollment Management', {
            'fields': ('enrolled_users', 'enrolled_users_display'),
            'description': 'Manage project enrollments and view enrolled users'
        }),
        ('Media', {
            'fields': ('cover_image', 'cover_image_url', 'cover_image_preview', 'video_urls'),
            'description': 'Upload an image, provide a URL for the cover image, or add video URLs'
        }),
        ('Scheduling & Status', {
            'fields': ('application_deadline', 'start_date', 'end_date', 'is_active', 'is_hero_highlight', 'is_featured'),
            'description': 'Important dates and visibility settings'
        }),
        ('Related Content', {
            'fields': ('success_stories_display',),
            'description': 'Success stories related to this project'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def headcount_display(self, obj):
        """Display headcount as current/total"""
        if obj.total_headcount > 0:
            percentage = (obj.headcount / obj.total_headcount) * 100
            color = 'green' if percentage < 80 else 'orange' if percentage < 100 else 'red'
            return format_html(
                '<span style="color: {};">{}/{}</span>',
                color,
                obj.headcount,
                obj.total_headcount
            )
        return f"{obj.headcount}/∞"
    headcount_display.short_description = 'Headcount'
    
    def image_preview(self, obj):
        """Display thumbnail of cover image"""
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image.url)
        elif obj.cover_image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image_url)
        return "No image"
    image_preview.short_description = 'Preview'

    def enrolled_count(self, obj):
        """Display number of enrolled users"""
        count = obj.enrolled_users.count()
        return count
    enrolled_count.short_description = 'Enrolled'
    
    def duration_display(self, obj):
        """Display duration in a formatted way"""
        if obj.duration:
            hours = obj.duration
            if hours < 24:
                return f"{hours}h"
            elif hours < 168:  # Less than a week
                days = hours / 24
                return f"{days:.1f}d"
            else:
                weeks = hours / 168
                return f"{weeks:.1f}w"
        return format_html('<span style="color: gray;">N/A</span>')
    duration_display.short_description = 'Duration'
    
    def status_display(self, obj):
        """Display project status based on dates"""
        from django.utils import timezone
        now = timezone.now()
        
        if obj.application_deadline and now > obj.application_deadline:
            return format_html('<span style="color: red;">⏰ Deadline Passed</span>')
        elif obj.is_full:
            return format_html('<span style="color: orange;">👥 Full</span>')
        elif obj.is_active:
            return format_html('<span style="color: green;">✓ Open</span>')
        else:
            return format_html('<span style="color: gray;">✗ Inactive</span>')
    status_display.short_description = 'Status'
    
    def enrolled_users_display(self, obj):
        """Display enrolled users in a styled table with user details"""
        if not obj.pk:
            return "Save the project first to manage enrollments"
        
        users = obj.enrolled_users.all()
        total_users = users.count()
        
        if not users:
            return format_html(
                '<div style="padding: 15px; background: #f8f9fa; border-left: 4px solid #6c757d; border-radius: 4px;">'
                '<p style="margin: 0; color: #6c757d;">👥 No users enrolled yet</p>'
                '</div>'
            )
        
        # Build the table
        html_parts = [
            '<div style="margin: 10px 0;">',
            f'<p style="font-weight: bold; margin-bottom: 10px;">📊 Total Enrolled: {total_users} / {obj.total_headcount if obj.total_headcount > 0 else "∞"}</p>',
            '<table style="width: 100%; border-collapse: collapse; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">',
            '<thead>',
            '<tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">',
            '<th style="padding: 12px; text-align: left; font-weight: 600;">#</th>',
            '<th style="padding: 12px; text-align: left; font-weight: 600;">👤 Username</th>',
            '<th style="padding: 12px; text-align: left; font-weight: 600;">📧 Email</th>',
            '<th style="padding: 12px; text-align: left; font-weight: 600;">⚙️ Actions</th>',
            '</tr>',
            '</thead>',
            '<tbody>',
        ]
        
        for idx, user in enumerate(users[:20], 1):  # Show first 20 users
            user_url = reverse('admin:users_customuser_change', args=[user.pk])
            row_style = 'background: #f8f9fa;' if idx % 2 == 0 else 'background: white;'
            
            html_parts.append(f'<tr style="{row_style}">')
            html_parts.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{idx}</td>')
            html_parts.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;"><strong>{user.username}</strong></td>')
            html_parts.append(f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">{user.email or "—"}</td>')
            html_parts.append(
                f'<td style="padding: 10px; border-bottom: 1px solid #dee2e6;">'
                f'<a href="{user_url}" style="color: #007bff; text-decoration: none;">View Profile →</a>'
                f'</td>'
            )
            html_parts.append('</tr>')
        
        html_parts.append('</tbody>')
        html_parts.append('</table>')
        
        if total_users > 20:
            html_parts.append(
                f'<p style="margin-top: 10px; padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">'
                f'<strong>ℹ️ Showing 20 of {total_users} enrolled users</strong></p>'
            )
        
        html_parts.append('</div>')
        
        return mark_safe(''.join(html_parts))
    
    enrolled_users_display.short_description = '👥 Enrolled Users'
    
    def success_stories_display(self, obj):
        """Display related success stories in a styled card layout"""
        if not obj.pk:
            return "Save the project first to view related stories"
        
        stories = obj.success_stories.all()
        total_stories = stories.count()
        
        if not stories:
            return format_html(
                '<div style="padding: 15px; background: #f8f9fa; border-left: 4px solid #6c757d; border-radius: 4px;">'
                '<p style="margin: 0; color: #6c757d;">📖 No success stories linked to this project yet</p>'
                '</div>'
            )
        
        # Build card layout
        html_parts = [
            '<div style="margin: 10px 0;">',
            f'<p style="font-weight: bold; margin-bottom: 15px;">📊 Total Success Stories: {total_stories}</p>',
            '<div style="display: grid; gap: 15px;">',
        ]
        
        for story in stories:
            story_url = reverse('admin:content_successstory_change', args=[story.pk])
            
            # Determine status badge
            if story.is_published:
                status_badge = '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: 600;">✓ PUBLISHED</span>'
            else:
                status_badge = '<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: 600;">○ DRAFT</span>'
            
            # Get metrics
            beneficiaries = f'{story.beneficiaries:,}' if story.beneficiaries else '—'
            hours = f'{story.total_hours_contributed:,}h' if story.total_hours_contributed else '—'
            
            # Image preview
            if story.cover_image:
                image_html = f'<img src="{story.cover_image.url}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px; margin-right: 15px;" />'
            elif story.cover_image_url:
                image_html = f'<img src="{story.cover_image_url}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 4px; margin-right: 15px;" />'
            else:
                image_html = '<div style="width: 80px; height: 80px; background: #e9ecef; border-radius: 4px; margin-right: 15px; display: flex; align-items: center; justify-content: center; font-size: 32px;">📖</div>'
            
            html_parts.append(
                f'<div style="border: 1px solid #dee2e6; border-radius: 6px; padding: 15px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; align-items: center;">'
                f'{image_html}'
                f'<div style="flex: 1;">'
                f'<div style="margin-bottom: 8px;">'
                f'<a href="{story_url}" style="font-size: 16px; font-weight: 600; color: #007bff; text-decoration: none;">{story.title}</a>'
                f'</div>'
                f'<div style="margin-bottom: 8px;">{status_badge}</div>'
                f'<div style="font-size: 13px; color: #6c757d;">'
                f'<span style="margin-right: 15px;">👥 <strong>{beneficiaries}</strong> beneficiaries</span>'
                f'<span>⏱️ <strong>{hours}</strong> contributed</span>'
                f'</div>'
                f'</div>'
                f'<a href="{story_url}" style="padding: 8px 16px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; font-size: 14px; white-space: nowrap;">View Story →</a>'
                f'</div>'
            )
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        
        return mark_safe(''.join(html_parts))
    
    success_stories_display.short_description = '📖 Success Stories'
    
    # Custom actions
    def mark_as_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} project(s) marked as active.')
    mark_as_active.short_description = 'Mark as active'
    
    def mark_as_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} project(s) marked as inactive.')
    mark_as_inactive.short_description = 'Mark as inactive'
    
    def set_as_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=True)
        self.message_user(request, f'{count} project(s) set as hero highlight.')
    set_as_hero_highlight.short_description = 'Set as hero highlight'
    
    def remove_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=False)
        self.message_user(request, f'{count} project(s) removed from hero highlight.')
    remove_hero_highlight.short_description = 'Remove hero highlight'
    
    def set_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} project(s) set as featured.')
    set_as_featured.short_description = 'Set as featured'
    
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} project(s) removed from featured.')
    remove_featured.short_description = 'Remove featured status'
    
    def duplicate_project(self, request, queryset):
        for project in queryset:
            # Create a duplicate
            project.pk = None
            project.project_id = ''
            project.kicc_project_id = None
            project.title = f"{project.title} (Copy)"
            project.save()
        self.message_user(request, f'{queryset.count()} project(s) duplicated successfully.')
    duplicate_project.short_description = 'Duplicate selected projects'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch"""
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('enrolled_users', 'success_stories')
        return qs

    def cover_image_preview(self, obj):
        """Show preview of cover image in detail view"""
        if obj.cover_image:
            return format_html('<img src="{}" width="200" />', obj.cover_image.url)
        if obj.cover_image_url:
            return format_html('<img src="{}" width="200" />', obj.cover_image_url)
        return "No image provided"
    cover_image_preview.short_description = 'Cover Preview'


class NewsEventGalleryImageInline(admin.TabularInline):
    """Inline admin for managing gallery images within NewsEvent admin"""
    model = NewsEventGalleryImage
    extra = 1
    fields = ('image_preview', 'caption', 'order')
    readonly_fields = ('image_preview',)
    ordering = ['order']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image / Not Saved Yet"
    image_preview.short_description = 'Preview'


@admin.register(NewsEvent)
class NewsEventAdmin(ExportMixin, TranslationAdmin):
    list_display = (
        'image_preview',
        'news_event_id', 
        'title_preview',
        'content_type', 
        'publish_date', 
        'is_published',
        'is_hero_highlight',
        'is_featured',
        'has_external_link',
        'created_at'
    )
    
    readonly_fields = (
        'news_event_id', 
        'updated_at',
        'cover_image_blob',
        'cover_image_blob_mime',
        'cover_image_blob_name',
        'cover_image_preview'
    )
    
    list_filter = (
        'content_type', 
        'is_published', 
        'is_hero_highlight', 
        'is_featured', 
        'publish_date',
        'created_at'
    )
    search_fields = ('title', 'body', 'news_event_id')
    ordering = ('-publish_date',)
    
    list_per_page = 50
    date_hierarchy = 'publish_date'
    save_on_top = True
    
    list_editable = ('is_published', 'is_hero_highlight', 'is_featured')
    
    inlines = [NewsEventGalleryImageInline]
    
    actions = [
        'export_as_csv',
        'publish_items',
        'unpublish_items',
        'set_as_hero_highlight',
        'remove_hero_highlight',
        'set_as_featured',
        'remove_featured'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('news_event_id',),
            'description': 'Unique identifier for this news/event'
        }),
        ('Content', {
            'fields': ('title', 'body', 'content_type'),
            'description': 'Main content and categorization'
        }),
        ('Media', {
            'fields': ('cover_image', 'cover_image_url', 'cover_image_preview', 'video_urls', 'external_link'),
            'description': 'Images, videos, and external resources'
        }),
        ('Publication', {
            'fields': ('publish_date', 'is_published', 'is_hero_highlight', 'is_featured'),
            'description': 'Publication settings and visibility'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_preview(self, obj):
        """Display truncated title"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Title'
    
    def has_external_link(self, obj):
        """Display if external link exists"""
        if obj.external_link:
            return format_html('✓ <a href="{}" target="_blank">Link</a>', obj.external_link)
        return format_html('<span style="color: gray;">—</span>')
    has_external_link.short_description = 'External Link'
    
    def image_preview(self, obj):
        """Display thumbnail of cover image"""
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image.url)
        elif obj.cover_image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image_url)
        return "No image"
    image_preview.short_description = 'Preview'
    
    # Custom actions
    def publish_items(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} item(s) published.')
    publish_items.short_description = 'Publish selected items'
    
    def unpublish_items(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} item(s) unpublished.')
    unpublish_items.short_description = 'Unpublish selected items'
    
    def set_as_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=True)
        self.message_user(request, f'{count} item(s) set as hero highlight.')
    set_as_hero_highlight.short_description = 'Set as hero highlight'
    
    def remove_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=False)
        self.message_user(request, f'{count} item(s) removed from hero highlight.')
    remove_hero_highlight.short_description = 'Remove hero highlight'
    
    def set_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} item(s) set as featured.')
    set_as_featured.short_description = 'Set as featured'
    
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} item(s) removed from featured.')
    remove_featured.short_description = 'Remove featured status'

    def cover_image_preview(self, obj):
        """Show preview of cover image in detail view"""
        if obj.cover_image:
            return format_html('<img src="{}" width="200" />', obj.cover_image.url)
        if obj.cover_image_url:
            return format_html('<img src="{}" width="200" />', obj.cover_image_url)
        return "No image provided"
    cover_image_preview.short_description = 'Cover Preview'


@admin.register(ProjectGalleryImage)
class ProjectGalleryImageAdmin(admin.ModelAdmin):
    """Admin for managing project gallery images"""
    list_display = ('id', 'project_link', 'image_preview', 'image_blob_name', 'caption', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title', 'caption', 'image_blob_name')
    readonly_fields = ('image_preview', 'image_blob', 'image_blob_mime', 'image_blob_name', 'updated_at')
    ordering = ('project', 'order', 'created_at')
    
    fieldsets = (
        ('Image Association', {
            'fields': ('project',),
        }),
        ('Image Data (Read-only)', {
            'fields': ('image_preview', 'image_blob_name', 'image_blob_mime'),
            'description': 'These fields are automatically populated from uploaded images'
        }),
        ('Image Details', {
            'fields': ('caption', 'order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def project_link(self, obj):
        """Display link to project"""
        if obj.project:
            url = reverse('admin:content_project_change', args=[obj.project.pk])
            return format_html('<a href="{}">{}</a>', url, obj.project.title[:40])
        return format_html('<span style="color: gray;">No project</span>')
    project_link.short_description = 'Project'

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(NewsEventGalleryImage)
class NewsEventGalleryImageAdmin(admin.ModelAdmin):
    """Admin for managing news/event gallery images"""
    list_display = ('id', 'news_event_link', 'image_preview', 'image_blob_name', 'caption', 'order', 'created_at')
    list_filter = ('news_event', 'created_at')
    search_fields = ('news_event__title', 'caption', 'image_blob_name')
    readonly_fields = ('image_preview', 'image_blob', 'image_blob_mime', 'image_blob_name', 'updated_at')
    ordering = ('news_event', 'order', 'created_at')
    
    fieldsets = (
        ('Image Association', {
            'fields': ('news_event',),
        }),
        ('Image Data (Read-only)', {
            'fields': ('image_preview', 'image_blob_name', 'image_blob_mime'),
            'description': 'These fields are automatically populated from uploaded images'
        }),
        ('Image Details', {
            'fields': ('caption', 'order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def news_event_link(self, obj):
        """Display link to news/event"""
        if obj.news_event:
            url = reverse('admin:content_newsevent_change', args=[obj.news_event.pk])
            return format_html('<a href="{}">{}</a>', url, obj.news_event.title[:40])
        return format_html('<span style="color: gray;">No news/event</span>')
    news_event_link.short_description = 'News/Event'

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image"
    image_preview.short_description = 'Preview'


@admin.register(SuccessStoryGalleryImage)
class SuccessStoryGalleryImageAdmin(admin.ModelAdmin):
    """Admin for managing success story gallery images"""
    list_display = ('id', 'success_story_link', 'image_preview', 'image_blob_name', 'caption', 'order', 'created_at')
    list_filter = ('success_story', 'created_at')
    search_fields = ('success_story__title', 'caption', 'image_blob_name')
    readonly_fields = ('image_preview', 'image_blob', 'image_blob_mime', 'image_blob_name', 'updated_at')
    ordering = ('success_story', 'order', 'created_at')
    
    fieldsets = (
        ('Image Association', {
            'fields': ('success_story',),
        }),
        ('Image Data (Read-only)', {
            'fields': ('image_preview', 'image_blob_name', 'image_blob_mime'),
            'description': 'These fields are automatically populated from uploaded images'
        }),
        ('Image Details', {
            'fields': ('caption', 'order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def success_story_link(self, obj):
        """Display link to success story"""
        if obj.success_story:
            url = reverse('admin:content_successstory_change', args=[obj.success_story.pk])
            return format_html('<a href="{}">{}</a>', url, obj.success_story.title[:40])
        return format_html('<span style="color: gray;">No story</span>')
    success_story_link.short_description = 'Success Story'

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image"
    image_preview.short_description = 'Preview'


class SuccessStoryGalleryImageInline(admin.TabularInline):
    """Inline admin for managing gallery images within SuccessStory admin"""
    model = SuccessStoryGalleryImage
    extra = 1
    fields = ('image_preview', 'caption', 'order')
    readonly_fields = ('image_preview',)
    ordering = ['order']

    def image_preview(self, obj):
        if obj.image_blob:
            encoded_image = base64.b64encode(obj.image_blob).decode('utf-8')
            return format_html(
                '<img src="data:{};base64,{}" width="150" />',
                obj.image_blob_mime,
                encoded_image
            )
        return "No Image / Not Saved Yet"
    image_preview.short_description = 'Preview'


@admin.register(SuccessStory)
class SuccessStoryAdmin(ExportMixin, TranslationAdmin):
    list_display = (
        'image_preview',
        'success_story_id', 
        'title_preview',
        'related_project_link',
        'beneficiaries_display',
        'hours_display',
        'media_count',
        'is_published',
        'is_hero_highlight',
        'is_featured',
        'published_at'
    )
    
    readonly_fields = (
        'success_story_id', 
        'updated_at',
        'cover_image_blob',
        'cover_image_blob_mime',
        'cover_image_blob_name',
        'cover_image_preview'
    )
    
    list_filter = (
        'is_published', 
        'is_hero_highlight', 
        'is_featured', 
        'related_project',
        'published_at',
        'created_at'
    )
    search_fields = ('title', 'body', 'success_story_id', 'related_project__title')
    ordering = ('-published_at',)
    
    list_per_page = 50
    date_hierarchy = 'published_at'
    save_on_top = True
    
    list_editable = ('is_published', 'is_hero_highlight', 'is_featured')
    
    autocomplete_fields = ['related_project']  # Requires search_fields in ProjectAdmin
    
    inlines = [SuccessStoryGalleryImageInline]
    
    actions = [
        'export_as_csv',
        'publish_stories',
        'unpublish_stories',
        'set_as_hero_highlight',
        'remove_hero_highlight',
        'set_as_featured',
        'remove_featured'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('success_story_id',),
            'description': 'Unique identifier for this success story'
        }),
        ('Content', {
            'fields': ('title', 'body', 'related_project'),
            'description': 'Story content and project relationship'
        }),
        ('Cover Media', {
            'fields': ('cover_image', 'cover_image_url', 'cover_image_preview'),
            'description': 'Main cover image for the story'
        }),
        ('Media Gallery', {
            'fields': ('image_urls', 'video_urls'),
            'description': 'Gallery images are managed below. Provide URLs for external images and videos here.',
            'classes': ('collapse',)
        }),
        ('Impact Metrics', {
            'fields': ('beneficiaries', 'total_hours_contributed'),
            'description': 'Quantify the impact of this success story'
        }),
        ('Publication', {
            'fields': ('is_published', 'is_hero_highlight', 'is_featured', 'published_at'),
            'description': 'Publication settings and visibility'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_preview(self, obj):
        """Display truncated title"""
        return obj.title[:40] + '...' if len(obj.title) > 40 else obj.title
    title_preview.short_description = 'Title'
    
    def related_project_link(self, obj):
        """Display link to related project"""
        if obj.related_project:
            url = reverse('admin:content_project_change', args=[obj.related_project.pk])
            return format_html('<a href="{}">{}</a>', url, obj.related_project.title[:30])
        return format_html('<span style="color: gray;">No project</span>')
    related_project_link.short_description = 'Related Project'
    
    def beneficiaries_display(self, obj):
        """Display beneficiaries count with formatting"""
        if obj.beneficiaries is not None and obj.beneficiaries > 0:
            return format_html('<strong>{}</strong>', f'{obj.beneficiaries:,}')
        return format_html('<span style="color: gray;">—</span>')
    beneficiaries_display.short_description = 'Beneficiaries'
    
    def hours_display(self, obj):
        """Display hours contributed"""
        if obj.total_hours_contributed is not None and obj.total_hours_contributed > 0:
            return format_html('<strong>{}h</strong>', f'{obj.total_hours_contributed:,}')
        return format_html('<span style="color: gray;">—</span>')
    hours_display.short_description = 'Hours'
    
    def media_count(self, obj):
        """Display count of media items"""
        image_count = len(obj.image_urls) if obj.image_urls else 0
        video_count = len(obj.video_urls) if obj.video_urls else 0
        # Add count of gallery images stored as blobs
        gallery_image_count = obj.gallery_images.count() if hasattr(obj, 'gallery_images') else 0
        image_count += gallery_image_count
        
        parts = []
        if image_count:
            parts.append(f'📷 {image_count}')
        if video_count:
            parts.append(f'🎥 {video_count}')
        
        if parts:
            return format_html(' '.join(parts))
        return format_html('<span style="color: gray;">—</span>')
    media_count.short_description = 'Media'
    
    def image_preview(self, obj):
        """Display thumbnail of cover image"""
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image.url)
        elif obj.cover_image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image_url)
        return "No image"
    image_preview.short_description = 'Preview'
    
    # Custom actions
    def publish_stories(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} story(ies) published.')
    publish_stories.short_description = 'Publish selected stories'
    
    def unpublish_stories(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} story(ies) unpublished.')
    unpublish_stories.short_description = 'Unpublish selected stories'
    
    def set_as_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=True)
        self.message_user(request, f'{count} story(ies) set as hero highlight.')
    set_as_hero_highlight.short_description = 'Set as hero highlight'
    
    def remove_hero_highlight(self, request, queryset):
        count = queryset.update(is_hero_highlight=False)
        self.message_user(request, f'{count} story(ies) removed from hero highlight.')
    remove_hero_highlight.short_description = 'Remove hero highlight'
    
    def set_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} story(ies) set as featured.')
    set_as_featured.short_description = 'Set as featured'
    
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} story(ies) removed from featured.')
    remove_featured.short_description = 'Remove featured status'

    def cover_image_preview(self, obj):
        """Show preview of cover image in detail view"""
        if obj.cover_image:
            return format_html('<img src="{}" width="200" />', obj.cover_image.url)
        if obj.cover_image_url:
            return format_html('<img src="{}" width="200" />', obj.cover_image_url)
        return "No image provided"
    cover_image_preview.short_description = 'Cover Preview'


@admin.register(FAQ)
class FAQAdmin(ExportMixin, TranslationAdmin):
    inlines = [FAQVoteInline]
    
    list_display = (
        'faq_id', 
        'question_preview', 
        'order', 
        'thumbs_up',
        'thumbs_down',
        'helpfulness_display',
        'is_schema_ready',
        'updated_at',
        'created_at'
    )
    
    readonly_fields = ('faq_id', 'updated_at', 'total_votes', 'helpfulness_ratio')
    
    list_filter = ('is_schema_ready', 'created_at', 'updated_at')
    search_fields = ('question', 'answer', 'faq_id')
    ordering = ('order',)
    
    list_per_page = 100
    list_editable = ('order', 'is_schema_ready')  # Allow quick reordering and schema toggle from list view
    save_on_top = True
    
    actions = [
        'export_as_csv',
        'enable_schema',
        'disable_schema',
        'reset_votes',
        'move_to_top',
        'move_to_bottom'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('faq_id',),
            'description': 'Unique identifier for this FAQ'
        }),
        ('Content', {
            'fields': ('question', 'answer'),
            'description': 'FAQ question and answer content'
        }),
        ('Settings', {
            'fields': ('order', 'is_schema_ready'),
            'description': 'Display order and SEO schema settings'
        }),
        ('User Feedback', {
            'fields': ('thumbs_up', 'thumbs_down', 'total_votes', 'helpfulness_ratio'),
            'classes': ('collapse',),
            'description': 'User feedback and helpfulness metrics'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        """Show truncated question"""
        return obj.question[:75] + '...' if len(obj.question) > 75 else obj.question
    question_preview.short_description = 'Question'
    
    def helpfulness_display(self, obj):
        """Display helpfulness ratio with color coding"""
        if obj.total_votes == 0:
            return format_html('<span style="color: gray;">No votes</span>')
        
        ratio = obj.helpfulness_ratio
        if ratio >= 80:
            color = 'green'
        elif ratio >= 60:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {};">{}% ({}/{})</span>',
            color,
            ratio,
            obj.thumbs_up,
            obj.total_votes
        )
    helpfulness_display.short_description = 'Helpfulness'
    
    # Custom actions
    def enable_schema(self, request, queryset):
        count = queryset.update(is_schema_ready=True)
        self.message_user(request, f'{count} FAQ(s) enabled for schema markup.')
    enable_schema.short_description = 'Enable schema markup'
    
    def disable_schema(self, request, queryset):
        count = queryset.update(is_schema_ready=False)
        self.message_user(request, f'{count} FAQ(s) disabled from schema markup.')
    disable_schema.short_description = 'Disable schema markup'
    
    def reset_votes(self, request, queryset):
        count = queryset.update(thumbs_up=0, thumbs_down=0)
        self.message_user(request, f'Votes reset for {count} FAQ(s).')
    reset_votes.short_description = 'Reset all votes'
    
    def move_to_top(self, request, queryset):
        """Move selected FAQs to the top of the list"""
        from django.db.models import Min
        min_order = FAQ.objects.aggregate(Min('order'))['order__min'] or 0
        
        for idx, faq in enumerate(queryset.order_by('order')):
            faq.order = min_order - len(queryset) + idx
            faq.save()
        
        self.message_user(request, f'{queryset.count()} FAQ(s) moved to top.')
    move_to_top.short_description = 'Move to top of list'
    
    def move_to_bottom(self, request, queryset):
        """Move selected FAQs to the bottom of the list"""
        from django.db.models import Max
        max_order = FAQ.objects.aggregate(Max('order'))['order__max'] or 0
        
        for idx, faq in enumerate(queryset.order_by('order')):
            faq.order = max_order + idx + 1
            faq.save()
        
        self.message_user(request, f'{queryset.count()} FAQ(s) moved to bottom.')
    move_to_bottom.short_description = 'Move to bottom of list'


@admin.register(FAQVote)
class FAQVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'faq', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at', 'faq')
    search_fields = ('user__username', 'user__email', 'faq__question')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Vote Details', {
            'fields': ('user', 'faq', 'vote_type'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'faq')


# Customize admin site branding with emojis
admin.site.site_header = "GDA 🛠️ Admin"
admin.site.index_title = "GDA"
admin.site.site_title = "Djanjgo Admin"
