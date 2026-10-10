from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Review, Comment, Endorsement
from .serializers import ReviewSerializer, CommentSerializer, EndorsementSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing project reviews."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'reviewer', 'status', 'is_endorsed']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        """Get reviews accessible to the user."""
        if self.request.user.role == 'FACULTY':
            return Review.objects.filter(reviewer=self.request.user)
        return Review.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        """Create review and set reviewer to current user."""
        serializer.save(reviewer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Faculty action: Approve review."""
        review = self.get_object()
        if request.user != review.reviewer:
            return Response(
                {'error': 'You can only approve your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        review.status = Review.ReviewStatus.APPROVED
        review.save()
        return Response({
            'message': 'Review approved',
            'review': ReviewSerializer(review).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def endorse(self, request, pk=None):
        """Faculty action: Endorse project from this review."""
        review = self.get_object()
        if request.user.role != 'FACULTY':
            return Response(
                {'error': 'Only faculty can endorse projects'},
                status=status.HTTP_403_FORBIDDEN
            )
        review.is_endorsed = True
        review.save()
        
        # Update project featured status
        project = review.project
        project.is_featured = True
        project.save()
        
        return Response({
            'message': 'Project endorsed',
            'review': ReviewSerializer(review).data
        })


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'review', 'author']
    ordering = ['-created_at']

    def get_queryset(self):
        """Get visible comments."""
        return Comment.objects.all()

    def perform_create(self, serializer):
        """Create comment with current user as author."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def edit(self, request, pk=None):
        """Edit own comment."""
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {'error': 'You can only edit your own comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.content = request.data.get('content', comment.content)
        comment.is_edited = True
        comment.save()
        return Response(CommentSerializer(comment).data)


class EndorsementViewSet(viewsets.ModelViewSet):
    """ViewSet for managing endorsements."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = EndorsementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'faculty']
    ordering = ['-created_at']

    def get_queryset(self):
        """Get endorsements visible to user."""
        return Endorsement.objects.all()

    def perform_create(self, serializer):
        """Create endorsement with current user as faculty."""
        if self.request.user.role != 'FACULTY':
            raise PermissionError("Only faculty can create endorsements.")
        serializer.save(faculty=self.request.user)


class ProjectReviewsView(generics.ListCreateAPIView):
    """List and create reviews for a specific project."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Get reviews for a specific project."""
        project_id = self.kwargs.get('project_id')
        return Review.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """Create review for project."""
        project_id = self.kwargs.get('project_id')
        serializer.save(reviewer=self.request.user, project_id=project_id)
