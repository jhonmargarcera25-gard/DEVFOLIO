from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with role and profile fields."""
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'student_id', 'department')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Email address'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Last name'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Student ID (if applicable)'
            }),
            'department': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Department'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class CustomUserChangeForm(UserChangeForm):
    """Custom user update form."""
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'student_id', 'department',
                  'bio', 'github_url', 'linkedin_url', 'avatar', 'phone_number', 'date_of_birth')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 4
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://github.com/username'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'type': 'date'
            }),
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    
    class Meta:
        model = UserProfile
        fields = ('specialization', 'institution', 'website')
        widgets = {
            'specialization': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'e.g., Web Development, Data Science'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Institution name'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'https://yourwebsite.com'
            }),
        }
