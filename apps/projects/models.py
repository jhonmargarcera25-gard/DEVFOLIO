from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


class Category(models.Model):
    """Project categories for organizing portfolio items."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default='folder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Student project submissions with multimedia support."""
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending Faculty Review'
        APPROVED = 'APPROVED', 'Approved / Featured'
        REJECTED = 'REJECTED', 'Needs Revision'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    abstract = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='projects'
    )
    academic_year = models.CharField(
        max_length=9,
        default='2025-2026',
        help_text='Format: YYYY-YYYY'
    )
    
    # Metadata & Links
    demo_link = models.URLField(blank=True, null=True)
    repo_link = models.URLField(blank=True, null=True)
    documentation_link = models.URLField(blank=True, null=True)
    
    # Status & Visibility
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    # Files with validation
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        help_text='Recommended: 16:9 aspect ratio, min 1200x675px'
    )
    model_3d_file = models.FileField(
        upload_to='projects/3d_models/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['glb', 'gltf'])],
        help_text='Upload .glb or .gltf file'
    )
    document_pdf = models.FileField(
        upload_to='projects/docs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Upload PDF documentation'
    )
    
    # Metadata
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text='Comma-separated tags'
    )
    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        help_text='Technologies used (comma-separated)'
    )
    team_members = models.CharField(
        max_length=255,
        blank=True,
        help_text='Team member names (comma-separated)'
    )
    
    # Engagement
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.title} - {self.owner.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_complete(self):
        """Check if all required fields are filled."""
        return all([self.title, self.abstract, self.category, self.thumbnail])


class ProjectGallery(models.Model):
    """Additional images/media gallery for projects."""
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='gallery'
    )
    image = models.ImageField(
        upload_to='projects/gallery/',
        help_text='Additional project images/screenshots'
    )
    title = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project Gallery'
        verbose_name_plural = 'Project Galleries'

    def __str__(self):
        return f"Gallery - {self.project.title}"
