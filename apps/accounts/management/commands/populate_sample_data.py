"""
Management command to create sample data for testing DevFolio.
Usage: python manage.py populate_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.projects.models import Category, Project
from apps.accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Starting sample data population...')

        # Create sample users
        self.create_users()
        
        # Create categories
        self.create_categories()
        
        # Create sample projects
        self.create_projects()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_users(self):
        """Create sample users with different roles."""
        users_data = [
            {
                'username': 'carlollobo',
                'email': 'carlollobo@gmail.com',
                'first_name': 'Carlo',
                'last_name': 'Llobo',
                'role': User.Role.STUDENT,
                'student_id': 'STU001',
                'department': 'Computer Science'
            },
            {
                'username': 'student2',
                'email': 'student2@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': User.Role.STUDENT,
                'student_id': 'STU002',
                'department': 'Information Technology'
            },
            {
                'username': 'faculty1',
                'email': 'faculty1@example.com',
                'first_name': 'Dr.',
                'last_name': 'Wilson',
                'role': User.Role.FACULTY,
                'department': 'Computer Science'
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True
            },
        ]

        for user_data in users_data:
            user = User.objects.filter(username=user_data['username']).first() or User.objects.filter(email=user_data['email']).first()
            if not user:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='testpass123',
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    role=user_data.get('role', User.Role.STUDENT),
                    student_id=user_data.get('student_id'),
                    department=user_data.get('department', 'BSIT'),
                    is_staff=user_data.get('is_staff', False),
                    is_superuser=user_data.get('is_superuser', False),
                    is_verified=True
                )
                user.set_password('testpass123')
                user.save()
            else:
                user.email = user_data['email']
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.role = user_data.get('role', user.role)
                user.student_id = user_data.get('student_id', user.student_id)
                user.department = user_data.get('department', user.department)
                user.is_staff = user_data.get('is_staff', user.is_staff)
                user.is_superuser = user_data.get('is_superuser', user.is_superuser)
                user.is_verified = True
                user.save()
            
            UserProfile.objects.get_or_create(user=user)
            
            self.stdout.write(f'Created/updated user: {user.username}')

    def create_categories(self):
        """Create default project categories."""
        categories_data = [
            {'name': 'Capstone Project', 'slug': 'capstone', 'description': 'Final year capstone projects'},
            {'name': 'Web Application', 'slug': 'web-app', 'description': 'Web development projects'},
            {'name': '3D Model', 'slug': '3d-model', 'description': '3D modeling and visualization'},
            {'name': 'Mobile App', 'slug': 'mobile-app', 'description': 'Mobile application development'},
            {'name': 'Data Science', 'slug': 'data-science', 'description': 'Data analysis and visualization'},
            {'name': 'AI/ML Project', 'slug': 'ai-ml', 'description': 'Machine learning projects'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

    def create_projects(self):
        """Create sample projects."""
        student1 = User.objects.get(username='student1')
        category = Category.objects.first()

        projects_data = [
            {
                'owner': student1,
                'title': 'E-Commerce Platform',
                'slug': 'ecommerce-platform',
                'abstract': 'A full-stack e-commerce platform built with Django and React',
                'description': 'A comprehensive e-commerce solution with user authentication, product catalog, shopping cart, and payment processing.',
                'category': category,
                'academic_year': '2025-2026',
                'status': Project.Status.APPROVED,
                'is_public': True,
                'demo_link': 'https://ecommerce-demo.example.com',
                'repo_link': 'https://github.com/example/ecommerce',
                'tech_stack': 'Django, React, PostgreSQL, Stripe',
                'tags': 'ecommerce, full-stack, payment',
            },
            {
                'owner': student1,
                'title': '3D Portfolio Viewer',
                'slug': '3d-portfolio-viewer',
                'abstract': 'Interactive 3D model viewer for portfolio items',
                'description': 'A Three.js based 3D viewer that allows users to interact with 3D models of portfolio items.',
                'category': category,
                'academic_year': '2025-2026',
                'status': Project.Status.APPROVED,
                'is_public': True,
                'is_featured': True,
                'demo_link': 'https://3d-viewer.example.com',
                'tech_stack': 'Three.js, WebGL, JavaScript',
                'tags': '3d, visualization, interactive',
            },
        ]

        for proj_data in projects_data:
            if not Project.objects.filter(slug=proj_data['slug']).exists():
                project = Project.objects.create(**proj_data)
                self.stdout.write(f'Created project: {project.title}')
