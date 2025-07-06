# TrackApply Deployment Guide

## Quick Start (Development)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd TrackApply
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create a production configuration**
   ```bash
   # Create gunicorn.conf.py
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "sync"
   timeout = 30
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -c gunicorn.conf.py app:app
   ```

### Environment Variables

Set these environment variables for production:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-super-secret-key-here
export DATABASE_URL=sqlite:///trackApply.db
```

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 5000

   CMD ["python", "app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t trackapply .
   docker run -p 5000:5000 trackapply
   ```

### Cloud Deployment Options

- **Heroku**: Push to Heroku with a `Procfile`
- **Railway**: Connect your GitHub repo
- **Render**: Deploy directly from GitHub
- **PythonAnywhere**: Upload files and configure WSGI

## Security Considerations

1. **Change the secret key** in production
2. **Use HTTPS** in production
3. **Set proper file permissions**
4. **Regular database backups**
5. **Monitor application logs**

## Database Backup

```bash
# Backup
cp trackApply.db trackApply_backup_$(date +%Y%m%d).db

# Restore
cp trackApply_backup_YYYYMMDD.db trackApply.db
```
