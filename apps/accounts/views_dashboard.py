from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from apps.projects.models import Project
from apps.reviews.models import Review


def login_view(request):
    """Render login page"""
    return render(request, 'accounts/login.html')


def register_view(request):
    """Render register page"""
    return render(request, 'accounts/register.html')


@login_required
def student_dashboard(request):
    """Render student dashboard HTML"""
    if request.user.role not in ['STUDENT', 'FACULTY']:
        return redirect('accounts:dashboard')

    user = request.user
    profile = UserProfile.objects.filter(user=user).first()

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/student_dashboard.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the student."""
    user = request.user

    projects = Project.objects.filter(owner=user)
    total_projects = projects.count()
    approved_projects = projects.filter(status='APPROVED').count()
    pending_projects = projects.filter(status='PENDING').count()

    reviews = Review.objects.filter(project__owner=user)
    total_reviews = reviews.count()
    avg_rating = 0.0
    if total_reviews > 0:
        total_score = sum(
            r.creativity + r.technical_quality + r.documentation + r.presentation
            for r in reviews
        )
        avg_rating = round(total_score / (total_reviews * 4), 2)

    profile = UserProfile.objects.filter(user=user).first()
    checks = [
        bool(user.first_name),
        bool(user.last_name),
        bool(user.email),
        bool(user.bio),
        bool(user.avatar),
        bool(profile and profile.specialization),
        bool(profile and profile.institution),
        bool(profile and profile.website),
    ]
    profile_complete = 0
    if checks:
        profile_complete = round((sum(checks) / len(checks)) * 100)

    return Response({
        'total_projects': total_projects,
        'approved_projects': approved_projects,
        'pending_projects': pending_projects,
        'total_reviews': total_reviews,
        'average_rating': avg_rating,
        'profile_completion': profile_complete,
    })
