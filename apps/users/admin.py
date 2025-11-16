from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Enhanced admin interface for CustomUser with all management capabilities
    """
    list_display = (
        'username',
        'email',
        'full_name_display',
        'contact_display',
        'gender',
        'blood_group',
        'enrolled_projects_count',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login_display'
    )
    
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'gender',
        'blood_group',
        'date_joined',
        'last_login'
    )
    
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'contact',
        'guardian_name',
        'address'
    )
    
    ordering = ('-date_joined',)
    
    list_per_page = 50
    
    date_hierarchy = 'date_joined'
    
    # Enable actions
    actions = [
        'activate_users',
        'deactivate_users',
        'make_staff',
        'remove_staff',
        'export_user_data'
    ]
    
    # Enhanced fieldsets for add/edit forms
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'gender')
        }),
        ('Contact Details', {
            'fields': ('country_code', 'contact', 'address')
        }),
        ('Medical Information', {
            'fields': ('blood_group',),
            'classes': ('collapse',)
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_relation'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Enrolled Projects', {
            'fields': ('enrolled_projects_display',),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Login Credentials', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'gender'),
        }),
        ('Contact Details', {
            'classes': ('wide',),
            'fields': ('country_code', 'contact', 'address'),
        }),
        ('Medical & Guardian Information', {
            'classes': ('wide', 'collapse'),
            'fields': ('blood_group', 'guardian_name', 'guardian_relation'),
        }),
        ('Permissions', {
            'classes': ('wide', 'collapse'),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'enrolled_projects_display')
    
    filter_horizontal = ('groups', 'user_permissions')
    
    # Custom display methods
    def full_name_display(self, obj):
        """Display full name with formatting"""
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return format_html('<span style="color: gray;">No name set</span>')
    full_name_display.short_description = 'Full Name'
    
    def contact_display(self, obj):
        """Display contact with country code"""
        if obj.contact:
            return f"{obj.country_code} {obj.contact}" if obj.country_code else obj.contact
        return format_html('<span style="color: gray;">No contact</span>')
    contact_display.short_description = 'Contact'
    
    def enrolled_projects_count(self, obj):
        """Display number of enrolled projects with color coding"""
        count = obj.enrolled_projects.count()
        if count == 0:
            color = 'gray'
        elif count <= 3:
            color = 'green'
        elif count <= 6:
            color = 'orange'
        else:
            color = 'blue'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    enrolled_projects_count.short_description = 'Enrolled Projects'
    
    def enrolled_projects_display(self, obj):
        """Display list of enrolled projects with links to admin"""
        from django.urls import reverse
        from django.utils.safestring import mark_safe
        
        if obj.pk:
            projects = obj.enrolled_projects.all()
            if projects:
                links = []
                for project in projects:
                    url = reverse('admin:content_project_change', args=[project.pk])
                    links.append(f'<li><a href="{url}">{project.title}</a></li>')
                return mark_safe('<ul style="margin: 0; padding-left: 20px;">' + ''.join(links) + '</ul>')
        return format_html('<span style="color: gray;">No projects enrolled</span>')
    enrolled_projects_display.short_description = 'Enrolled Projects List'
    
    def last_login_display(self, obj):
        """Display last login with formatting"""
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M')
        return format_html('<span style="color: gray;">Never</span>')
    last_login_display.short_description = 'Last Login'
    
    # Custom actions
    def activate_users(self, request, queryset):
        """Activate selected users"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} user(s) successfully activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} user(s) successfully deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def make_staff(self, request, queryset):
        """Grant staff status to selected users"""
        count = queryset.update(is_staff=True)
        self.message_user(request, f'{count} user(s) granted staff status.')
    make_staff.short_description = 'Grant staff status'
    
    def remove_staff(self, request, queryset):
        """Remove staff status from selected users"""
        count = queryset.update(is_staff=False)
        self.message_user(request, f'{count} user(s) removed from staff.')
    remove_staff.short_description = 'Remove staff status'
    
    def export_user_data(self, request, queryset):
        """Export selected user data (placeholder for CSV/Excel export)"""
        self.message_user(
            request,
            f'{queryset.count()} user(s) selected for export. (Export functionality to be implemented)',
            level='info'
        )
    export_user_data.short_description = 'Export user data'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch for enrolled projects"""
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('enrolled_projects')
        return qs
