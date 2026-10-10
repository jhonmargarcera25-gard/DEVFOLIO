"""
Celery tasks for DevFolio
"""

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.projects.models import Project
from PIL import Image
import os


@shared_task
def send_approval_email(project_id, approver_name):
    """Send email notification when project is approved."""
    try:
        project = Project.objects.get(id=project_id)
        
        subject = f"Your Project '{project.title}' has been Approved!"
        
        html_message = render_to_string('emails/project_approved.html', {
            'student_name': project.owner.get_full_name(),
            'project_title': project.title,
            'approver_name': approver_name,
            'project_url': f'https://yourdomain.com/projects/{project.slug}/'
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            'noreply@devfolio.com',
            [project.owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Email sent to {project.owner.email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"


@shared_task
def send_review_notification(review_id):
    """Send notification when a review is received."""
    from apps.reviews.models import Review
    
    try:
        review = Review.objects.get(id=review_id)
        
        subject = f"New Review on '{review.project.title}' by {review.reviewer.get_full_name()}"
        
        html_message = render_to_string('emails/new_review.html', {
            'student_name': review.project.owner.get_full_name(),
            'reviewer_name': review.reviewer.get_full_name(),
            'project_title': review.project.title,
            'rating': review.rating,
            'comment': review.comment[:200] + '...' if len(review.comment) > 200 else review.comment,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            'noreply@devfolio.com',
            [review.project.owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Review notification sent to {review.project.owner.email}"
    except Exception as e:
        return f"Error sending review notification: {str(e)}"


@shared_task
def generate_project_thumbnail(project_id):
    """Generate thumbnail from project image (if needed)."""
    try:
        project = Project.objects.get(id=project_id)
        
        if project.thumbnail:
            img = Image.open(project.thumbnail.path)
            img.thumbnail((400, 225))
            img.save(project.thumbnail.path, quality=85, optimize=True)
            
        return f"Thumbnail generated for project {project.title}"
    except Exception as e:
        return f"Error generating thumbnail: {str(e)}"


@shared_task
def send_endorsement_notification(endorsement_id):
    """Send notification when a project is endorsed."""
    from apps.reviews.models import Endorsement
    
    try:
        endorsement = Endorsement.objects.get(id=endorsement_id)
        
        subject = f"Your Project '{endorsement.project.title}' has been Endorsed!"
        
        html_message = render_to_string('emails/project_endorsed.html', {
            'student_name': endorsement.project.owner.get_full_name(),
            'project_title': endorsement.project.title,
            'faculty_name': endorsement.faculty.get_full_name(),
            'endorsement_text': endorsement.endorsement_text,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            'noreply@devfolio.com',
            [endorsement.project.owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return f"Endorsement notification sent to {endorsement.project.owner.email}"
    except Exception as e:
        return f"Error sending endorsement notification: {str(e)}"
