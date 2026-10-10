# DevFolio - Deployment Guide

## Local Development Setup

### 1. PostgreSQL Installation
```bash
# Windows (using PostgreSQL installer or WSL)
# Download from https://www.postgresql.org/download/windows/

# Linux
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

### 2. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE devfolio_db;
CREATE USER devfolio_user WITH PASSWORD 'your-password';
ALTER ROLE devfolio_user SET client_encoding TO 'utf8';
ALTER ROLE devfolio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE devfolio_user SET default_transaction_deferrable TO on;
ALTER ROLE devfolio_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE devfolio_db TO devfolio_user;
\q
```

### 3. Django Setup
```bash
cd DevFolio_web_based

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data (optional)
python manage.py populate_sample_data

# Run development server
python manage.py runserver
```

Access at: `http://localhost:8000/`
Admin panel: `http://localhost:8000/admin/`

---

## Docker Deployment

### 1. Build and Run with Docker Compose
```bash
cd DevFolio_web_based

# Build images
docker-compose build

# Start services
docker-compose up

# Run migrations (in another terminal)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py populate_sample_data
```

Access at: `http://localhost:8000/`

### 2. Stop Services
```bash
docker-compose down
```

---

## Production Deployment (Linux Server)

### 1. Server Setup
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.11 python3-pip python3-venv postgresql nginx supervisor redis-server
```

### 2. PostgreSQL Production Setup
```bash
sudo -u postgres psql
CREATE DATABASE devfolio_db;
CREATE USER devfolio_user WITH PASSWORD 'strong-password-here';
ALTER ROLE devfolio_user SET client_encoding TO 'utf8';
ALTER ROLE devfolio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE devfolio_user SET default_transaction_deferrable TO on;
ALTER ROLE devfolio_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE devfolio_db TO devfolio_user;
```

### 3. Application Setup
```bash
# Clone repository
git clone your-repo-url devfolio
cd devfolio

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure production settings
cp .env.example .env
# Edit .env - set DEBUG=False, SECRET_KEY, allowed hosts, database config

# Create necessary directories
mkdir -p logs media staticfiles

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. Gunicorn Configuration
Create `/etc/supervisor/conf.d/devfolio.conf`:
```ini
[program:devfolio]
directory=/home/user/devfolio
command=/home/user/devfolio/venv/bin/gunicorn devfolio.wsgi:application --bind 127.0.0.1:8000 --workers 4
user=user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/user/devfolio/logs/gunicorn.log
```

### 5. Nginx Configuration
Create `/etc/nginx/sites-available/devfolio`:
```nginx
upstream devfolio_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    client_max_body_size 50M;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /home/user/devfolio/staticfiles/;
        expires 30d;
    }

    # Media files
    location /media/ {
        alias /home/user/devfolio/media/;
        expires 7d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://devfolio_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/devfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 7. Start Services
```bash
# Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start devfolio

# Check status
sudo supervisorctl status devfolio
sudo journalctl -u supervisor -f

# View logs
tail -f /home/user/devfolio/logs/gunicorn.log
```

---

## AWS Deployment (Optional)

### 1. EC2 Setup
```bash
# Launch EC2 instance (Ubuntu 22.04)
# Configure security group:
# - HTTP (80)
# - HTTPS (443)
# - SSH (22)
```

### 2. RDS Database
```bash
# Create RDS PostgreSQL instance
# Database name: devfolio_db
# Master username: devfolio_user
# Add to same VPC as EC2
```

### 3. S3 Media Storage
```bash
# Create S3 bucket for media
# Create IAM user with S3 access
# Update .env with AWS credentials
```

### 4. Update settings.py for S3
```python
# In production settings
if USE_S3:
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
        },
    }
```

---

## Monitoring & Maintenance

### 1. Database Backups
```bash
# Daily backup
0 2 * * * pg_dump -U devfolio_user devfolio_db > /backups/devfolio_$(date +\%Y\%m\%d).sql

# Upload to S3
aws s3 cp /backups/devfolio_*.sql s3://your-backup-bucket/
```

### 2. Log Rotation
Create `/etc/logrotate.d/devfolio`:
```
/home/user/devfolio/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0600 user user
    sharedscripts
}
```

### 3. Health Check
```bash
# Monitor application health
curl -I https://yourdomain.com/api/showcase/statistics/
```

### 4. Performance Monitoring
```bash
# Install monitoring tools
sudo apt-get install htop iotop nethogs

# Monitor Gunicorn processes
top -p $(pgrep -f gunicorn | tr '\n' ',' | sed 's/,$//')
```

---

## Troubleshooting

### Connection Refused
```bash
# Check if Gunicorn is running
sudo supervisorctl status devfolio

# Restart
sudo supervisorctl restart devfolio
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Check Nginx config
sudo nginx -t
```

### Database Connection Error
```bash
# Test connection
python manage.py dbshell

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Media Upload Issues
```bash
# Check permissions
ls -la media/
chmod 755 media/

# Check disk space
df -h
```

---

## Scaling Considerations

1. **Database**: Use read replicas for scaling read operations
2. **Cache**: Implement Redis for session and query caching
3. **CDN**: Use CloudFront/Cloudflare for static and media files
4. **Load Balancing**: Use AWS ELB or Nginx upstream for multiple app servers
5. **Celery**: Use for async tasks (email, thumbnails, etc.)

---

## Support

For deployment issues, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/
- PostgreSQL: https://www.postgresql.org/docs/
