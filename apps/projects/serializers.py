from rest_framework import serializers
from .models import Category, Project, ProjectGallery


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class ProjectGallerySerializer(serializers.ModelSerializer):
    """Serializer for ProjectGallery model."""
    
    class Meta:
        model = ProjectGallery
        fields = ['id', 'image', 'title', 'order', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""
    
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    owner_avatar = serializers.URLField(source='owner.avatar.url', read_only=True, allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    gallery = ProjectGallerySerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'owner_name', 'owner_avatar', 'title', 'slug',
            'abstract', 'description', 'category', 'category_name',
            'academic_year', 'demo_link', 'repo_link', 'documentation_link',
            'status', 'is_featured', 'is_public', 'thumbnail',
            'model_3d_file', 'document_pdf', 'tech_stack', 'tags',
            'team_members', 'views_count', 'likes_count', 'gallery',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'id', 'owner', 'slug', 'views_count', 'likes_count',
            'created_at', 'updated_at', 'published_at'
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    """Simplified serializer for project lists."""
    
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'abstract', 'thumbnail',
            'owner', 'owner_name', 'category', 'category_name',
            'status', 'views_count', 'likes_count', 'created_at'
        ]
