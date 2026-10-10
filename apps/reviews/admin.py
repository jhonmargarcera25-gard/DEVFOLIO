from django.contrib import admin
from .models import Review, Comment, Endorsement


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review model."""
    
    list_display = ('project', 'reviewer', 'rating', 'status', 'is_endorsed', 'created_at')
    list_filter = ('status', 'is_endorsed', 'rating', 'created_at')
    search_fields = ('project__title', 'reviewer__username', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'average_criteria_score')
    
    fieldsets = (
        ('Review Details', {
            'fields': ('project', 'reviewer', 'rating', 'comment', 'status')
        }),
        ('Criteria Scores', {
            'fields': ('creativity', 'technical_quality', 'documentation', 'presentation', 'average_criteria_score')
        }),
        ('Endorsement', {
            'fields': ('is_endorsed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    
    list_display = ('author', 'get_target', 'is_edited', 'created_at')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_target(self, obj):
        return obj.project or obj.review
    get_target.short_description = 'Target'


@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    """Admin interface for Endorsement model."""
    
    list_display = ('project', 'faculty', 'featured_until', 'created_at')
    list_filter = ('created_at', 'featured_until')
    search_fields = ('project__title', 'faculty__username')
    readonly_fields = ('created_at', 'updated_at')
