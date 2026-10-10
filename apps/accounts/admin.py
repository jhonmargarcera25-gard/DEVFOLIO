from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin interface for User model."""
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')}),
        ('Role & Department', {'fields': ('role', 'student_id', 'department')}),
        ('Bio & Links', {'fields': ('bio', 'github_url', 'linkedin_url', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    list_display = ('username', 'email', 'get_full_name', 'role', 'student_id', 'is_verified', 'created_at')
    list_filter = ('role', 'is_active', 'is_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    
    list_display = ('get_user', 'specialization', 'institution', 'is_featured', 'profile_views', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('user__username', 'user__email', 'specialization', 'institution')
    readonly_fields = ('profile_views', 'created_at', 'updated_at')
    
    def get_user(self, obj):
        return obj.user.get_full_name()
    get_user.short_description = 'User'
