# DevFolio - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- pip and virtualenv

### Step 1: Setup
```bash
cd DevFolio_web_based
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Database Configuration
```bash
# Create .env file from example
cp .env.example .env

# Edit .env with your database credentials:
# DB_USER=devfolio_user
# DB_PASSWORD=your_password
# DB_NAME=devfolio_db
# DB_HOST=localhost

# In PostgreSQL:
# CREATE DATABASE devfolio_db;
# CREATE USER devfolio_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE devfolio_db TO devfolio_user;
```

### Step 3: Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_sample_data
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Access Application
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Docs**: http://localhost:8000/api/showcase/statistics/

---

## 📝 Test Login Credentials

After running `populate_sample_data`:

| Role | Username | Password |
|------|----------|----------|
| Student | student1 | testpass123 |
| Student | student2 | testpass123 |
| Faculty | faculty1 | testpass123 |
| Admin | admin | testpass123 |

---

## 🐳 Docker Quick Start

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py populate_sample_data
```

Access at: http://localhost:8000/

---

## 📚 Project Structure

```
apps/
├── accounts/     → User management & authentication
├── projects/     → Project submissions & portfolio
├── reviews/      → Faculty reviews & endorsements
└── showcase/     → Public gallery & search
```

---

## 🔑 Key Features

✅ Role-based authentication (Student, Faculty, Employer, Admin)
✅ Rich multimedia uploads (3D models, PDFs, images)
✅ Project categorization and tagging
✅ Faculty review system with criteria scoring
✅ Public gallery and search functionality
✅ Endorsement workflow
✅ RESTful API with comprehensive endpoints
✅ Admin interface for management

---

## 📖 Documentation

- **API Docs**: See `API_DOCUMENTATION.md`
- **Deployment**: See `DEPLOYMENT.md`
- **README**: See `README.md`

---

## 🐛 Troubleshooting

### Connection Error
```bash
# Make sure PostgreSQL is running
sudo service postgresql start  # Linux
brew services start postgresql  # macOS
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Permission Denied (Media Folder)
```bash
mkdir -p media staticfiles
chmod 755 media staticfiles
```

---

## 📞 Support

For issues or questions, check:
1. `.env` file configuration
2. Database connection
3. Django logs: `python manage.py runserver` output
4. Admin panel status

---

## 🎯 Next Steps

1. **Customize branding**: Update admin site title in settings
2. **Configure email**: Set up email backend for notifications
3. **Add frontend**: Build UI using Tailwind CSS + Alpine.js or React
4. **Deploy**: Follow `DEPLOYMENT.md` for production setup
5. **Customize models**: Extend models in each app as needed

---

## 📚 Learning Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- PostgreSQL Docs: https://www.postgresql.org/docs/

Enjoy building with DevFolio! 🎓✨
