from django.contrib import admin
from .models import Category, Project, ProjectGallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model."""
    
    list_display = ('title', 'owner', 'category', 'status', 'is_featured', 'views_count', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'created_at', 'academic_year')
    search_fields = ('title', 'abstract', 'owner__username', 'owner__email')
    readonly_fields = ('views_count', 'likes_count', 'slug', 'created_at', 'updated_at', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Project Information', {
            'fields': ('owner', 'title', 'slug', 'abstract', 'description', 'category')
        }),
        ('Links & References', {
            'fields': ('demo_link', 'repo_link', 'documentation_link')
        }),
        ('Media Files', {
            'fields': ('thumbnail', 'model_3d_file', 'document_pdf')
        }),
        ('Details', {
            'fields': ('tech_stack', 'tags', 'team_members', 'academic_year')
        }),
        ('Status & Engagement', {
            'fields': ('status', 'is_featured', 'is_public', 'views_count', 'likes_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectGallery)
class ProjectGalleryAdmin(admin.ModelAdmin):
    """Admin interface for ProjectGallery model."""
    
    list_display = ('project', 'title', 'order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title', 'title')
    ordering = ('project', 'order')
