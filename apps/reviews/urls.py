from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reviews'

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'endorsements', views.EndorsementViewSet, basename='endorsement')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_id>/reviews/', views.ProjectReviewsView.as_view(), name='project_reviews'),
]
