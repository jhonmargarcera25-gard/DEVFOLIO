# DevFolio Project Structure & File Guide

## Complete Directory Tree

```
DevFolio_web_based/
│
├── manage.py                              # Django management script
├── requirements.txt                       # Python dependencies
├── .env.example                           # Environment variables template
├── .gitignore                             # Git ignore rules
│
├── Dockerfile                             # Docker image configuration
├── docker-compose.yml                     # Multi-container setup
│
├── README.md                              # Project overview
├── QUICKSTART.md                          # Quick start guide
├── DEPLOYMENT.md                          # Production deployment guide
├── API_DOCUMENTATION.md                   # API reference
│
├── devfolio/                              # Project Core
│   ├── __init__.py
│   ├── settings.py                        # Django settings (DB, apps, middleware)
│   ├── urls.py                            # Main URL routing
│   ├── wsgi.py                            # WSGI application
│   └── celery.py                          # Celery configuration
│
├── apps/                                  # Django Applications
│   ├── __init__.py
│   │
│   ├── accounts/                          # User Management
│   │   ├── __init__.py
│   │   ├── apps.py                        # App configuration
│   │   ├── models.py                      # User, UserProfile models
│   │   ├── forms.py                       # Registration, profile forms
│   │   ├── views.py                       # Auth views, profile endpoints
│   │   ├── serializers.py                 # REST serializers
│   │   ├── urls.py                        # App URL routing
│   │   ├── admin.py                       # Admin interface
│   │   ├── signals.py                     # Signal handlers (create profile on user creation)
│   │   └── management/
│   │       └── commands/
│   │           └── populate_sample_data.py # Sample data generation
│   │
│   ├── projects/                          # Project Management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                      # Project, Category, ProjectGallery models
│   │   ├── forms.py                       # Project submission forms
│   │   ├── views.py                       # Project CRUD, filtering, approval
│   │   ├── serializers.py                 # REST serializers (detailed, list versions)
│   │   ├── urls.py                        # Project API routes
│   │   ├── admin.py                       # Admin interface
│   │   └── tasks.py                       # Celery tasks (emails, thumbnails)
│   │
│   ├── reviews/                           # Review & Endorsement System
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                      # Review, Comment, Endorsement models
│   │   ├── views.py                       # Review management, endorsement workflow
│   │   ├── serializers.py                 # REST serializers
│   │   ├── urls.py                        # Review API routes
│   │   └── admin.py                       # Admin interface
│   │
│   └── showcase/                          # Public Gallery & Search
│       ├── __init__.py
│       ├── apps.py
│       ├── views.py                       # Public APIs (gallery, search, analytics)
│       └── urls.py                        # Public route definitions
│
├── templates/                             # Django HTML Templates
│   ├── base.html                          # Base template
│   ├── accounts/                          # Account templates
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── projects/                          # Project templates
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── create_edit.html
│   ├── reviews/                           # Review templates
│   │   └── review_list.html
│   ├── showcase/                          # Public gallery
│   │   ├── gallery.html
│   │   └── search.html
│   └── emails/                            # Email templates
│       ├── project_approved.html
│       ├── new_review.html
│       └── project_endorsed.html
│
├── static/                                # Static Files (CSS, JS, Images)
│   ├── css/
│   │   ├── tailwind.css                   # Tailwind CSS
│   │   └── custom.css                     # Custom styles
│   ├── js/
│   │   ├── three.js                       # 3D model viewer
│   │   ├── alpine.js                      # Alpine.js for interactivity
│   │   └── main.js                        # Custom scripts
│   └── images/
│       └── logo.png
│
├── media/                                 # User Uploads (Generated at Runtime)
│   ├── avatars/                           # User profile pictures
│   ├── projects/
│   │   ├── thumbnails/                    # Project thumbnails
│   │   ├── 3d_models/                     # .glb, .gltf files
│   │   ├── docs/                          # PDF documentation
│   │   └── gallery/                       # Additional project images
│   └── files/                             # Other uploads
│
└── staticfiles/                           # Collected static files (Production)
```

---

## File Descriptions

### Core Configuration Files

#### `manage.py`
- Django command-line utility
- Run migrations, create superuser, start server

#### `settings.py`
- Database configuration (PostgreSQL)
- Installed apps (accounts, projects, reviews, showcase)
- Middleware, templates, static/media settings
- REST Framework configuration
- CORS, security settings
- Email backend configuration

#### `urls.py`
- Main URL dispatcher
- Routes all app URLs under `/api/` prefix
- Serves media files in development

#### `wsgi.py`
- WSGI application entry point
- Used by production servers (Gunicorn, uWSGI)

#### `celery.py`
- Celery worker configuration
- Async task processing (emails, thumbnails)

---

### App: Accounts (User Management)

#### `models.py`
- **User**: Custom user model with roles (Student, Faculty, Employer, Admin)
  - Fields: role, student_id, department, bio, social links, avatar
  - Methods: is_student(), is_faculty(), is_employer(), is_admin_user()
- **UserProfile**: Extended profile for additional metadata
  - Fields: specialization, institution, website, profile_views

#### `views.py`
- `RegisterView`: User registration
- `LoginView`: User authentication
- `LogoutView`: Session termination
- `CurrentUserView`: Get authenticated user
- `UserProfileView`: View profile by ID
- `UserProfileUpdateView`: Update own profile
- `StudentListView`: Directory of students
- `FacultyListView`: Directory of faculty

#### `serializers.py`
- `UserSerializer`: Full user representation with profile
- `UserProfileSerializer`: Profile data only

#### `forms.py`
- `CustomUserCreationForm`: Registration form with role selection
- `CustomUserChangeForm`: Profile update form
- `UserProfileForm`: Profile metadata form

#### `urls.py`
- Registration, login, logout endpoints
- Profile viewing and updates
- Student/Faculty directory listing

#### `admin.py`
- Custom User admin with enhanced list display
- UserProfile admin interface

#### `signals.py`
- Auto-create UserProfile when User is created
- User-profile synchronization

---

### App: Projects (Portfolio Management)

#### `models.py`
- **Category**: Project categories (Capstone, Web App, 3D Model, etc.)
- **Project**: Main project model
  - Fields: owner, title, abstract, category, academic_year, status
  - File fields: thumbnail, 3d_model, pdf_document
  - Engagement: views_count, likes_count
  - Metadata: tags, tech_stack, team_members
  - Status workflow: DRAFT → PENDING → APPROVED/REJECTED
- **ProjectGallery**: Additional images for projects

#### `views.py`
- `CategoryViewSet`: Browse categories
- `ProjectViewSet`: Full CRUD with filtering
  - Actions: approve (faculty), reject (faculty), like, view
- `ProjectGalleryViewSet`: Manage gallery images
- `UserProjectsView`: User's own projects

#### `serializers.py`
- `ProjectSerializer`: Full project details
- `ProjectListSerializer`: Simplified for lists
- `CategorySerializer`: Category data
- `ProjectGallerySerializer`: Gallery items

#### `forms.py`
- `ProjectForm`: Project submission form with media fields
- `ProjectGalleryForm`: Gallery image form
- `ProjectFilterForm`: Filter/search form

#### `urls.py`
- Project CRUD endpoints
- Category browsing
- My projects endpoint

#### `tasks.py`
- `send_approval_email`: Notification on approval
- `send_review_notification`: Review received notification
- `generate_project_thumbnail`: Image optimization
- `send_endorsement_notification`: Endorsement notification

#### `admin.py`
- Category admin with slug auto-population
- Project admin with detailed fieldsets
- Gallery admin with ordering

---

### App: Reviews (Evaluation System)

#### `models.py`
- **Review**: Faculty reviews with rating and criteria scores
  - Fields: project, reviewer, rating, comment, status
  - Criteria: creativity, technical_quality, documentation, presentation
  - Endorsement flag for featured projects
- **Comment**: Discussion threads on reviews/projects
  - Fields: content, author, target (project or review)
- **Endorsement**: Faculty endorsements
  - Fields: project, faculty, text, featured_until

#### `views.py`
- `ReviewViewSet`: Manage reviews with approval/endorsement
- `CommentViewSet`: Comment management with edit capability
- `EndorsementViewSet`: Manage endorsements
- `ProjectReviewsView`: Get reviews for specific project

#### `serializers.py`
- `ReviewSerializer`: Full review with comments and scores
- `CommentSerializer`: Comment data
- `EndorsementSerializer`: Endorsement data

#### `urls.py`
- Review management endpoints
- Comment creation/editing
- Endorsement tracking
- Project-specific review routes

#### `admin.py`
- Review admin with criteria display
- Comment admin with target tracking
- Endorsement admin with featured tracking

---

### App: Showcase (Public Gallery)

#### `views.py`
- `PublicProjectListView`: Approved projects gallery
- `FeaturedProjectsView`: Top featured projects
- `ProjectDetailView`: Public project detail (increments views)
- `PublicStudentDirectoryView`: Students with projects
- `PublicFacultyDirectoryView`: Faculty directory
- `CategoryDetailView`: Category with all projects
- `search_view`: Global search (projects, students, faculty)
- `showcase_statistics_view`: Analytics dashboard

#### `urls.py`
- Public project gallery
- Student/faculty directories
- Search endpoint
- Analytics endpoint
- Category browsing

---

## Database Schema Relationships

```
User (1) ──→ (M) Project
User (1) ──→ (M) Review (as reviewer)
User (1) ──→ (1) UserProfile
User (1) ──→ (M) Comment

Project (1) ──→ (M) Review
Project (1) ──→ (M) ProjectGallery
Project (1) ──→ (M) Comment
Project (M) ──→ (1) Category
Project (1) ──→ (M) Endorsement

Review (1) ──→ (M) Comment
Review (M) ──→ (1) Endorsement (one-to-one unique)

Comment (M) ──→ (1) Project
Comment (M) ──→ (1) Review
Comment (M) ──→ (1) Author (User)
```

---

## Environment Variables (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=devfolio_db
DB_USER=devfolio_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## API Routes Summary

```
/api/
├── accounts/
│   ├── register/
│   ├── login/
│   ├── logout/
│   ├── me/
│   ├── profile/<id>/
│   ├── profile/update/
│   ├── students/
│   └── faculty/
│
├── projects/
│   ├── (list, create, detail, update, delete)
│   ├── categories/
│   ├── <id>/approve/
│   ├── <id>/reject/
│   ├── <id>/like/
│   ├── gallery/ (CRUD)
│   └── my-projects/
│
├── reviews/
│   ├── reviews/ (CRUD)
│   ├── reviews/<id>/approve/
│   ├── reviews/<id>/endorse/
│   ├── comments/ (CRUD)
│   ├── endorsements/ (CRUD)
│   └── projects/<id>/reviews/
│
└── showcase/
    ├── projects/ (public list)
    ├── projects/featured/
    ├── projects/<slug>/
    ├── students/
    ├── faculty/
    ├── categories/<slug>/
    ├── search/
    └── statistics/
```

---

## Common Operations

### Creating a New Feature
1. Create models in `apps/[feature]/models.py`
2. Create serializers in `apps/[feature]/serializers.py`
3. Create views in `apps/[feature]/views.py`
4. Add URLs in `apps/[feature]/urls.py`
5. Register in admin in `apps/[feature]/admin.py`
6. Run migrations: `python manage.py makemigrations [feature]`

### Adding New Endpoints
1. Create view method/class in views.py
2. Add URL pattern in urls.py
3. Create/update serializer if needed
4. Test with: `python manage.py runserver`

### Modifying Models
1. Update model in models.py
2. Create migration: `python manage.py makemigrations`
3. Apply: `python manage.py migrate`
4. Update serializers and admin if needed

---

## File Sizes & Performance Notes

- **Database**: PostgreSQL handles 100k+ projects efficiently
- **Media Storage**: Use S3/CDN in production for media files
- **Static Files**: Collect to staticfiles/ for production serving
- **Caching**: Implement Redis for session/query caching
- **Tasks**: Celery for async operations (emails, image processing)

---

This structure follows Django best practices with clear separation of concerns, scalable architecture, and comprehensive feature coverage for portfolio management.
