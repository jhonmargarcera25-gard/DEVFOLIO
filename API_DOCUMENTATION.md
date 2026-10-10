# DevFolio API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

### Session Authentication (Web)
Include session cookies in requests after login.

### Example Login Flow
```bash
# 1. Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"testpass123"}' \
  -c cookies.txt

# 2. Use cookies in subsequent requests
curl http://localhost:8000/api/projects/my-projects/ \
  -b cookies.txt
```

---

## Accounts API

### Register User
**POST** `/accounts/register/`

Request:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password1": "secure_pass123",
  "password2": "secure_pass123",
  "first_name": "John",
  "last_name": "Llobo",
  "role": "STUDENT",
  "student_id": "STU123",
  "department": "Computer Science"
}
```

Response (201):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "STUDENT",
    "created_at": "2025-10-05T10:30:00Z"
  }
}
```

### Login
**POST** `/accounts/login/`

Request:
```json
{
  "username": "student1",
  "password": "testpass123"
}
```

Response (200):
```json
{
  "message": "Login successful",
  "user": { ... }
}
```

### Get Current User
**GET** `/accounts/me/`

Response (200):
```json
{
  "id": 1,
  "username": "student1",
  "email": "student1@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "STUDENT",
  "bio": "Passionate developer",
  "avatar": "http://localhost:8000/media/avatars/user.jpg",
  "profile": {
    "specialization": "Web Development",
    "institution": "University",
    "website": "https://example.com"
  }
}
```

### Update Profile
**PUT** `/accounts/profile/update/`

Request:
```json
{
  "first_name": "John",
  "bio": "Updated bio",
  "github_url": "https://github.com/johndoe"
}
```

### List Students
**GET** `/accounts/students/`

Query Parameters:
- `search` - Search by username, email, or name
- `ordering` - Order by field

Response (200):
```json
[
  {
    "id": 1,
    "username": "student1",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "STU001",
    "department": "Computer Science"
  }
]
```

### List Faculty
**GET** `/accounts/faculty/`

---

## Projects API

### List Projects
**GET** `/projects/`

Query Parameters:
- `category` - Filter by category ID
- `status` - Filter by status (DRAFT, PENDING, APPROVED, REJECTED)
- `academic_year` - Filter by academic year
- `search` - Search in title, abstract, tags
- `ordering` - Order by field
- `page` - Page number

Response (200):
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "E-Commerce Platform",
      "slug": "e-commerce-platform",
      "abstract": "A full-stack e-commerce solution",
      "thumbnail": "http://localhost:8000/media/projects/thumbnails/thumb.jpg",
      "owner": 1,
      "owner_name": "John Doe",
      "category": 1,
      "category_name": "Web Application",
      "status": "APPROVED",
      "views_count": 150,
      "likes_count": 25,
      "created_at": "2025-10-01T10:00:00Z"
    }
  ]
}
```

### Get Single Project
**GET** `/projects/{id}/`

Response (200):
```json
{
  "id": 1,
  "owner": 1,
  "owner_name": "John Doe",
  "owner_avatar": "http://localhost:8000/media/avatars/user.jpg",
  "title": "E-Commerce Platform",
  "slug": "e-commerce-platform",
  "abstract": "A full-stack e-commerce solution",
  "description": "Comprehensive description...",
  "category": 1,
  "category_name": "Web Application",
  "academic_year": "2025-2026",
  "demo_link": "https://demo.example.com",
  "repo_link": "https://github.com/example/project",
  "documentation_link": "https://docs.example.com",
  "status": "APPROVED",
  "is_featured": true,
  "is_public": true,
  "thumbnail": "http://localhost:8000/media/projects/thumbnails/thumb.jpg",
  "model_3d_file": "http://localhost:8000/media/projects/3d_models/model.glb",
  "document_pdf": "http://localhost:8000/media/projects/docs/doc.pdf",
  "tech_stack": "Django, React, PostgreSQL",
  "tags": "ecommerce, full-stack",
  "team_members": "John Doe, Jane Smith",
  "views_count": 150,
  "likes_count": 25,
  "gallery": [
    {
      "id": 1,
      "image": "http://localhost:8000/media/projects/gallery/img1.jpg",
      "title": "Homepage Screenshot",
      "order": 1
    }
  ],
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-05T15:30:00Z"
}
```

### Create Project
**POST** `/projects/`

Requires authentication. Multipart form data.

Request:
```
title: "E-Commerce Platform"
abstract: "A full-stack e-commerce solution"
description: "Comprehensive description..."
category: 1
academic_year: "2025-2026"
thumbnail: [file]
model_3d_file: [file] (optional)
document_pdf: [file] (optional)
demo_link: "https://demo.example.com"
repo_link: "https://github.com/..."
tech_stack: "Django, React"
tags: "ecommerce, full-stack"
is_public: true
```

Response (201):
```json
{
  "id": 2,
  "owner": 1,
  "title": "E-Commerce Platform",
  "status": "DRAFT",
  ...
}
```

### Update Project
**PUT** `/projects/{id}/`

Requires authentication and ownership.

### Delete Project
**DELETE** `/projects/{id}/`

Requires authentication and ownership.

### Approve Project (Faculty Only)
**POST** `/projects/{id}/approve/`

Response (200):
```json
{
  "message": "Project approved",
  "project": { ... }
}
```

### Reject Project (Faculty Only)
**POST** `/projects/{id}/reject/`

Request:
```json
{
  "reason": "Missing documentation"
}
```

### Like Project
**POST** `/projects/{id}/like/`

Response (200):
```json
{
  "message": "Project liked",
  "likes_count": 26
}
```

### Get My Projects
**GET** `/projects/my-projects/`

Requires authentication.

---

## Reviews API

### List Reviews
**GET** `/reviews/reviews/`

Query Parameters:
- `project` - Filter by project ID
- `status` - Filter by status
- `is_endorsed` - Filter by endorsement status

Response (200):
```json
[
  {
    "id": 1,
    "project": 1,
    "reviewer": 2,
    "reviewer_name": "Dr. Wilson",
    "rating": 5,
    "comment": "Excellent work!",
    "creativity": 9,
    "technical_quality": 9,
    "documentation": 8,
    "presentation": 9,
    "average_criteria_score": 8.75,
    "is_endorsed": true,
    "status": "APPROVED",
    "created_at": "2025-10-03T12:00:00Z"
  }
]
```

### Create Review
**POST** `/reviews/reviews/`

Requires authentication. Faculty only.

Request:
```json
{
  "project": 1,
  "rating": 5,
  "comment": "Excellent project!",
  "creativity": 9,
  "technical_quality": 9,
  "documentation": 8,
  "presentation": 9
}
```

Response (201):
```json
{
  "id": 2,
  "project": 1,
  "reviewer": 2,
  "rating": 5,
  ...
}
```

### Endorse Project
**POST** `/reviews/reviews/{id}/endorse/`

Requires authentication. Faculty only.

Response (200):
```json
{
  "message": "Project endorsed",
  "review": { ... }
}
```

### Get Project Reviews
**GET** `/reviews/projects/{project_id}/reviews/`

### Comment on Review
**POST** `/reviews/comments/`

Request:
```json
{
  "review": 1,
  "content": "Great observation!"
}
```

Response (201):
```json
{
  "id": 1,
  "author": 1,
  "author_name": "John Doe",
  "content": "Great observation!",
  "is_edited": false,
  "created_at": "2025-10-05T14:00:00Z"
}
```

---

## Showcase API (Public)

### List Public Projects
**GET** `/showcase/projects/`

Public endpoint. Same filters as projects API.

### Featured Projects
**GET** `/showcase/projects/featured/`

Returns top 12 featured projects.

### Project Detail (Public)
**GET** `/showcase/projects/{slug}/`

Access by project slug instead of ID.

### Student Directory
**GET** `/showcase/students/`

List students with public projects.

### Faculty Directory
**GET** `/showcase/faculty/`

List all faculty members.

### Search
**GET** `/showcase/search/?q=query`

Query Parameters:
- `q` - Search query (minimum 2 characters)

Response (200):
```json
{
  "query": "django",
  "projects": [ ... ],
  "students": [ ... ],
  "faculty": [ ... ],
  "total_results": 15
}
```

### Statistics
**GET** `/showcase/statistics/`

Response (200):
```json
{
  "total_projects": 45,
  "total_students": 120,
  "categories_count": 6,
  "categories": [
    {
      "name": "Web Application",
      "count": 15
    }
  ],
  "top_viewed_projects": [ ... ]
}
```

---

## Categories API

### List Categories
**GET** `/projects/categories/`

Response (200):
```json
[
  {
    "id": 1,
    "name": "Capstone Project",
    "slug": "capstone",
    "description": "Final year capstone projects",
    "icon": "award"
  }
]
```

### Category Detail
**GET** `/showcase/categories/{slug}/`

Response (200):
```json
{
  "category": {
    "name": "Web Application",
    "slug": "web-app",
    "description": "Web development projects",
    "icon": "globe"
  },
  "projects": [ ... ],
  "project_count": 15
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": { ... }
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

To implement rate limiting, add to settings:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## Pagination

Default pagination returns 20 items per page. Include in response:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/projects/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

To change page size:
```
GET /api/projects/?page_size=50
```

---

## Testing API

### Using cURL
```bash
curl -X GET http://localhost:8000/api/projects/ \
  -H "Content-Type: application/json"
```

### Using Python Requests
```python
import requests

response = requests.get('http://localhost:8000/api/projects/')
data = response.json()
print(data)
```

### Using Postman
1. Import OpenAPI/Swagger spec
2. Set environment variables for base URL
3. Use pre-request scripts for authentication

---

## WebSocket Support (Optional)

For real-time notifications, implement WebSockets:
```python
# Install: pip install channels
# Add to settings: INSTALLED_APPS += ['daphne']
```

---

## Changelog

- **v1.0.0** (2025-10-05): Initial API release
