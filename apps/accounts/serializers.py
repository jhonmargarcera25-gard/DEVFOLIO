from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = ['specialization', 'institution', 'website', 'profile_views', 'is_featured']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'student_id', 'department', 'bio', 'github_url',
            'linkedin_url', 'avatar', 'phone_number', 'date_of_birth',
            'is_verified', 'profile', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']
