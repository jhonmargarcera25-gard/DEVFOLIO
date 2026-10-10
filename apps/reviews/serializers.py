from rest_framework import serializers
from .models import Review, Comment, Endorsement


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_avatar = serializers.URLField(source='author.avatar.url', read_only=True, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'author_avatar', 'content', 'is_edited', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'is_edited', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    reviewer_avatar = serializers.URLField(source='reviewer.avatar.url', read_only=True, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'project', 'reviewer', 'reviewer_name', 'reviewer_avatar',
            'rating', 'comment', 'status', 'creativity', 'technical_quality',
            'documentation', 'presentation', 'average_criteria_score',
            'is_endorsed', 'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'status', 'created_at', 'updated_at']


class EndorsementSerializer(serializers.ModelSerializer):
    """Serializer for Endorsement model."""
    
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    
    class Meta:
        model = Endorsement
        fields = ['id', 'project', 'faculty', 'faculty_name', 'endorsement_text', 'featured_until', 'created_at']
        read_only_fields = ['id', 'faculty', 'created_at']
