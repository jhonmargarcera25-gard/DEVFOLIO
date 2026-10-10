from django.urls import path
from . import views

app_name = 'showcase'

urlpatterns = [
    # Public galleries
    path('projects/', views.PublicProjectListView.as_view(), name='project_list'),
    path('projects/featured/', views.FeaturedProjectsView.as_view(), name='featured'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Public directories
    path('students/', views.PublicStudentDirectoryView.as_view(), name='student_directory'),
    path('faculty/', views.PublicFacultyDirectoryView.as_view(), name='faculty_directory'),
    
    # Categories
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Search & Analytics
    path('search/', views.search_view, name='search'),
    path('statistics/', views.showcase_statistics_view, name='statistics'),
]
