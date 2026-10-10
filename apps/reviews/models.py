from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Faculty reviews and endorsements for projects."""
    
    class ReviewStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    class RatingChoices(models.IntegerChoices):
        ONE = 1, '⭐'
        TWO = 2, '⭐⭐'
        THREE = 3, '⭐⭐⭐'
        FOUR = 4, '⭐⭐⭐⭐'
        FIVE = 5, '⭐⭐⭐⭐⭐'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        limit_choices_to={'role': 'FACULTY'}
    )
    
    rating = models.IntegerField(
        choices=RatingChoices.choices,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING
    )
    
    # Criteria Scores
    creativity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Innovation and originality (0-10)'
    )
    technical_quality = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Code quality and implementation (0-10)'
    )
    documentation = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Documentation completeness (0-10)'
    )
    presentation = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Presentation quality (0-10)'
    )
    
    # Is Endorsed
    is_endorsed = models.BooleanField(
        default=False,
        help_text='Faculty endorsement for featured projects'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'reviewer']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['reviewer', '-created_at']),
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"Review of {self.project.title} by {self.reviewer.get_full_name()}"

    @property
    def average_criteria_score(self):
        """Calculate average of criteria scores."""
        total = self.creativity + self.technical_quality + self.documentation + self.presentation
        return total / 4 if total > 0 else 0


class Comment(models.Model):
    """Comments on projects or reviews."""
    
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        target = self.project or self.review
        return f"Comment by {self.author.get_full_name()} on {target}"


class Endorsement(models.Model):
    """Faculty endorsements for student projects."""
    
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='endorsements'
    )
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='endorsements_given',
        limit_choices_to={'role': 'FACULTY'}
    )
    
    endorsement_text = models.TextField()
    featured_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date until which project should be featured'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'faculty']
        verbose_name = 'Endorsement'
        verbose_name_plural = 'Endorsements'

    def __str__(self):
        return f"Endorsement for {self.project.title} by {self.faculty.get_full_name()}"
