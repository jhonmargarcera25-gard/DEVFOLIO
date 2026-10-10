from django import forms
from .models import Project, ProjectGallery, Category


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""
    
    tech_stack = forms.CharField(
        required=False,
        help_text='Enter technologies separated by commas',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'Django, React, PostgreSQL, Three.js'
        })
    )
    tags = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'portfolio, web, 3d-model'
        })
    )
    team_members = forms.CharField(
        required=False,
        help_text='Enter team member names separated by commas',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'John Doe, Jane Smith'
        })
    )

    class Meta:
        model = Project
        fields = [
            'title', 'abstract', 'description', 'category',
            'academic_year', 'demo_link', 'repo_link', 'documentation_link',
            'thumbnail', 'model_3d_file', 'document_pdf',
            'tech_stack', 'tags', 'team_members', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Project title'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 3,
                'placeholder': 'Brief description of your project'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 5,
                'placeholder': 'Detailed project description'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': '2025-2026'
            }),
            'demo_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://project-demo.com'
            }),
            'repo_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://github.com/username/project'
            }),
            'documentation_link': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://docs.example.com'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4'
            }),
        }


class ProjectGalleryForm(forms.ModelForm):
    """Form for project gallery items."""
    
    class Meta:
        model = ProjectGallery
        fields = ['image', 'title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Image title'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
        }


class ProjectFilterForm(forms.Form):
    """Form for filtering projects."""
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg'
        })
    )
    academic_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'Academic year'
        })
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg',
            'placeholder': 'Search projects...'
        })
    )
