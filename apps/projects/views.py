from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import Category, Project, ProjectGallery
from .serializers import (
    CategorySerializer, ProjectSerializer,
    ProjectListSerializer, ProjectGallerySerializer
)
from .forms import ProjectForm, ProjectGalleryForm


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing project categories."""
    
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing projects."""
    
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'academic_year', 'is_featured']
    search_fields = ['title', 'abstract', 'description', 'tags', 'tech_stack']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use simplified serializer for list views."""
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_permissions(self):
        """Allow any user to retrieve projects."""
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Set the owner to the current user."""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Ensure only owner can update."""
        if serializer.instance.owner != self.request.user:
            raise PermissionError("You can only edit your own projects.")
        serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Faculty action: Approve project."""
        project = self.get_object()
        if request.user.role != 'FACULTY':
            return Response(
                {'error': 'Only faculty can approve projects'},
                status=status.HTTP_403_FORBIDDEN
            )
        project.status = Project.Status.APPROVED
        project.published_at = timezone.now()
        project.save()
        return Response({
            'message': 'Project approved',
            'project': ProjectSerializer(project).data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Faculty action: Reject project."""
        project = self.get_object()
        if request.user.role != 'FACULTY':
            return Response(
                {'error': 'Only faculty can reject projects'},
                status=status.HTTP_403_FORBIDDEN
            )
        reason = request.data.get('reason', 'No reason provided')
        project.status = Project.Status.REJECTED
        project.save()
        return Response({
            'message': f'Project rejected. Reason: {reason}',
            'project': ProjectSerializer(project).data
        })

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a project."""
        project = self.get_object()
        project.likes_count += 1
        project.save()
        return Response({
            'message': 'Project liked',
            'likes_count': project.likes_count
        })

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        """Increment view counter."""
        project = self.get_object()
        project.views_count += 1
        project.save()
        return Response(ProjectSerializer(project).data)


class ProjectGalleryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing project gallery items."""
    
    permission_classes = [IsAuthenticated]
    queryset = ProjectGallery.objects.all()
    serializer_class = ProjectGallerySerializer

    def get_queryset(self):
        """Filter gallery by project."""
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return ProjectGallery.objects.filter(project_id=project_id)
        return ProjectGallery.objects.all()

    def perform_create(self, serializer):
        """Ensure owner permission."""
        project = serializer.validated_data.get('project')
        if project.owner != self.request.user:
            raise PermissionError("You can only add images to your own projects.")
        serializer.save()


class UserProjectsView(generics.ListCreateAPIView):
    """List user's own projects or create new."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Get projects of the authenticated user."""
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Create project for current user."""
        serializer.save(owner=self.request.user)
