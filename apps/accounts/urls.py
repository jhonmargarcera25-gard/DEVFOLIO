from django.urls import path
from . import views
from .views_dashboard import student_dashboard, dashboard_stats, login_view, register_view

app_name = 'accounts'

urlpatterns = [
    # Frontend Pages
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    
    # API Authentication
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User Management
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('me/', views.CurrentUserView.as_view(), name='current_user'),
    
    # Dashboard
    path('dashboard/', student_dashboard, name='dashboard'),
    path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    
    # Student Directory
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('faculty/', views.FacultyListView.as_view(), name='faculty_list'),
]
