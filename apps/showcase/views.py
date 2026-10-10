from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg

from apps.projects.models import Project, Category
from apps.projects.serializers import ProjectListSerializer, ProjectSerializer
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User


class PublicProjectListView(generics.ListAPIView):
    """Public gallery of approved projects."""
    
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'academic_year']
    search_fields = ['title', 'abstract', 'tags', 'tech_stack']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']
    pagination_class = None  # Can be configured per deployment

    def get_queryset(self):
        """Only return approved and public projects."""
        return Project.objects.filter(
            status=Project.Status.APPROVED,
            is_public=True
        ).select_related('owner', 'category')


class FeaturedProjectsView(generics.ListAPIView):
    """Featured/endorsed projects showcase."""
    
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        """Return featured approved projects."""
        return Project.objects.filter(
            status=Project.Status.APPROVED,
            is_featured=True,
            is_public=True
        ).annotate(
            total_likes=Count('likes_count')
        ).order_by('-total_likes', '-created_at')[:12]


class ProjectDetailView(generics.RetrieveAPIView):
    """Detailed view of a single public project."""
    
    permission_classes = [AllowAny]
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(
        status=Project.Status.APPROVED,
        is_public=True
    )
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Increment view counter on retrieve."""
        response = super().retrieve(request, *args, **kwargs)
        project = self.get_object()
        project.views_count += 1
        project.save(update_fields=['views_count'])
        return response


class PublicStudentDirectoryView(generics.ListAPIView):
    """Public directory of students with featured projects."""
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'student_id', 'department']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return students with public projects."""
        return User.objects.filter(
            role=User.Role.STUDENT,
            is_active=True,
            projects__status=Project.Status.APPROVED,
            projects__is_public=True
        ).distinct()


class PublicFacultyDirectoryView(generics.ListAPIView):
    """Public directory of faculty members."""
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'department']
    ordering = ['-created_at']

    def get_queryset(self):
        return User.objects.filter(
            role=User.Role.FACULTY,
            is_active=True
        )


class CategoryDetailView(generics.RetrieveAPIView):
    """Category with all projects in that category."""
    
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        """Return category and its projects."""
        category = self.get_object()
        projects = Project.objects.filter(
            category=category,
            status=Project.Status.APPROVED,
            is_public=True
        )
        return Response({
            'category': {
                'name': category.name,
                'slug': category.slug,
                'description': category.description,
                'icon': category.icon,
            },
            'projects': ProjectListSerializer(projects, many=True).data,
            'project_count': projects.count()
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def search_view(request):
    """Global search across projects, students, and faculty."""
    query = request.query_params.get('q', '').strip()
    
    if len(query) < 2:
        return Response({
            'error': 'Search query must be at least 2 characters',
            'projects': [],
            'students': [],
            'faculty': []
        })
    
    # Search projects
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(abstract__icontains=query) |
        Q(tags__icontains=query),
        status=Project.Status.APPROVED,
        is_public=True
    )[:10]
    
    # Search students
    students = User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(student_id__icontains=query),
        role=User.Role.STUDENT,
        is_active=True,
        projects__status=Project.Status.APPROVED,
        projects__is_public=True
    ).distinct()[:10]
    
    # Search faculty
    faculty = User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query),
        role=User.Role.FACULTY,
        is_active=True
    )[:10]
    
    return Response({
        'query': query,
        'projects': ProjectListSerializer(projects, many=True).data,
        'students': UserSerializer(students, many=True).data,
        'faculty': UserSerializer(faculty, many=True).data,
        'total_results': projects.count() + students.count() + faculty.count()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def showcase_statistics_view(request):
    """Showcase statistics and analytics."""
    
    total_projects = Project.objects.filter(
        status=Project.Status.APPROVED,
        is_public=True
    ).count()
    
    total_students = User.objects.filter(
        role=User.Role.STUDENT,
        is_active=True,
        projects__status=Project.Status.APPROVED,
        projects__is_public=True
    ).distinct().count()
    
    categories = Category.objects.annotate(
        project_count=Count('projects', filter=Q(projects__status=Project.Status.APPROVED))
    )
    
    top_projects = Project.objects.filter(
        status=Project.Status.APPROVED,
        is_public=True
    ).order_by('-views_count')[:5]
    
    return Response({
        'total_projects': total_projects,
        'total_students': total_students,
        'categories_count': categories.count(),
        'categories': [
            {'name': cat.name, 'count': cat.project_count}
            for cat in categories
        ],
        'top_viewed_projects': ProjectListSerializer(top_projects, many=True).data
    })
