# DevFolio - Django-Based Portfolio Showcase Platform

A comprehensive Django application for managing and showcasing student projects with multimedia support, faculty reviews, and role-based access control.

## Features

### 🎓 Multi-Role Authentication System
- **Students**: Create and manage portfolios
- **Faculty/Advisors**: Review and endorse projects
- **Employers/Guests**: Browse and search projects
- **Administrators**: Manage platform and content

### 📁 Rich Multimedia Support
- 3D Model uploads (.glb, .gltf) with Three.js rendering
- Image galleries for projects
- PDF documentation uploads
- Project thumbnails and demo links

### 🎨 Project Management
- Project categorization (Capstone, Web App, 3D Model, Mobile App, etc.)
- Multiple file types per project
- Rich tagging and technology stack documentation
- Team member tracking
- Status workflow (Draft → Pending → Approved/Rejected)

### ⭐ Faculty Review System
- Detailed project reviews with ratings
- Criteria-based scoring (Creativity, Technical Quality, Documentation, Presentation)
- Faculty endorsements for featured projects
- Comment threads on reviews

### 📊 Public Showcase
- Approved projects gallery
- Featured projects section
- Student directory
- Faculty directory
- Global search functionality
- Analytics dashboard

## Project Structure

```
devfolio_project/
├── manage.py
├── devfolio/                   # Project Core
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/               # User Management & Authentication
│   │   ├── models.py          (User, UserProfile)
│   │   ├── views.py           (Registration, Login, Profiles)
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── projects/               # Project Management
│   │   ├── models.py          (Project, Category, ProjectGallery)
│   │   ├── views.py           (Project CRUD, Filtering)
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── reviews/                # Review & Endorsement System
│   │   ├── models.py          (Review, Comment, Endorsement)
│   │   ├── views.py           (Review Management)
│   │   ├── serializers.py
│   │   └── urls.py
│   └── showcase/               # Public Gallery & Search
│       ├── views.py           (Public APIs, Search, Analytics)
│       └── urls.py
├── templates/                  # Django Templates
├── media/                      # Uploaded Assets
├── static/                     # CSS, JavaScript
├── requirements.txt
└── .env.example
```

## Database Schema

### User Model
- Role-based access (Student, Faculty, Employer, Admin)
- Student ID, Department, Bio
- Social links (GitHub, LinkedIn)
- Avatar/Profile image

### Project Model
- Owner (ForeignKey to User)
- Title, Abstract, Description
- Category (ForeignKey)
- Status workflow (Draft, Pending, Approved, Rejected)
- Multiple file fields (Thumbnail, 3D Model, PDF)
- Metadata (Tags, Tech Stack, Team Members)
- Engagement tracking (Views, Likes)

### Review Model
- Project & Reviewer (Faculty) references
- Rating & detailed comment
- Criteria scores (Creativity, Technical Quality, Documentation, Presentation)
- Endorsement flag
- Status tracking

### Other Models
- **Category**: Project categorization
- **ProjectGallery**: Additional project images
- **UserProfile**: Extended user metadata
- **Comment**: Discussion threads
- **Endorsement**: Faculty endorsements with featured periods

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET /api/accounts/me/` - Current user info

### Projects
- `GET /api/projects/` - List all projects (with filters)
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Project detail
- `PUT /api/projects/{id}/` - Update project
- `POST /api/projects/{id}/approve/` - Faculty approval
- `POST /api/projects/{id}/reject/` - Faculty rejection
- `POST /api/projects/{id}/like/` - Like project

### Reviews
- `GET /api/reviews/reviews/` - List reviews
- `POST /api/reviews/reviews/` - Create review
- `POST /api/reviews/reviews/{id}/endorse/` - Endorse project

### Public Showcase
- `GET /api/showcase/projects/` - Public project gallery
- `GET /api/showcase/projects/featured/` - Featured projects
- `GET /api/showcase/projects/{slug}/` - Project detail (public)
- `GET /api/showcase/students/` - Student directory
- `GET /api/showcase/faculty/` - Faculty directory
- `GET /api/showcase/search/?q=query` - Global search
- `GET /api/showcase/statistics/` - Analytics

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip and virtualenv

### Installation

1. **Clone and Setup Virtual Environment**
```bash
cd DevFolio_web_based
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

4. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. **Create Default Categories**
```bash
python manage.py shell
```
```python
from apps.projects.models import Category

categories = [
    {'name': 'Capstone Project', 'slug': 'capstone'},
    {'name': 'Web Application', 'slug': 'web-app'},
    {'name': '3D Model', 'slug': '3d-model'},
    {'name': 'Mobile App', 'slug': 'mobile-app'},
    {'name': 'Data Science', 'slug': 'data-science'},
    {'name': 'AI/ML Project', 'slug': 'ai-ml'},
]

for cat in categories:
    Category.objects.get_or_create(**cat)
```

6. **Run Development Server**
```bash
python manage.py runserver
```

Access the admin panel at `http://localhost:8000/admin/`

## Frontend Integration

### REST API Configuration
The backend provides a comprehensive REST API for frontend integration:
- Base URL: `http://localhost:8000/api/`
- Authentication: Session-based for web, Token-based for mobile (optional)
- CORS enabled for frontend domains

### Frontend Technologies (Recommended)
- **Tailwind CSS** - Styling
- **Alpine.js** - Lightweight interactivity
- **Three.js** - 3D model rendering
- **React/Vue** - Advanced UI (optional)

### Media File Serving
- Development: Django serves media files
- Production: Configure S3 or CDN for media storage

## Security Considerations

1. **Database**
   - Use strong, unique passwords
   - Run on private networks in production

2. **File Uploads**
   - Validate file types and sizes
   - Store outside webroot in production
   - Use S3/CDN for public files

3. **API Security**
   - Implement rate limiting
   - Use HTTPS in production
   - Validate CORS origins
   - Implement CSRF protection

4. **User Management**
   - Implement email verification
   - Use strong password requirements
   - Implement account lockout after failed attempts

## Development Tips

### Creating Fixtures
```bash
python manage.py dumpdata apps.projects > fixtures/projects.json
python manage.py loaddata fixtures/projects.json
```

### Running Tests
```bash
python manage.py test apps.accounts
python manage.py test apps.projects
```

### Code Formatting
```bash
black .
isort .
flake8
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure strong `SECRET_KEY`
- [ ] Set up PostgreSQL
- [ ] Configure S3/CDN for media
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend
- [ ] Set up error logging (Sentry)
- [ ] Use Gunicorn/uWSGI
- [ ] Configure Nginx/Apache
- [ ] Set up cron jobs for maintenance

### Docker Deployment (Optional)
See `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push and create Pull Request

## License

This project is part of the DevFolio platform.

## Support

For issues and questions, please contact the development team.
