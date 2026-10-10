from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'projects'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'', views.ProjectViewSet, basename='project')
router.register(r'gallery', views.ProjectGalleryViewSet, basename='gallery')

urlpatterns = [
    path('', include(router.urls)),
    path('my-projects/', views.UserProjectsView.as_view(), name='my_projects'),
]
