# TrackApply Deployment Guide

## 🚀 One-Click Deployment

### Deploy to Heroku (Recommended)

Click the button below to deploy TrackApply to Heroku instantly:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Shadshere/Track-Apply)

### Manual Heroku Deployment

1. **Create a Heroku account** at [heroku.com](https://heroku.com)

2. **Install Heroku CLI**
   - Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

3. **Login to Heroku**
   ```bash
   heroku login
   ```

4. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

5. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
   heroku config:set FLASK_ENV=production
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Open your app**
   ```bash
   heroku open
   ```

## 🖥️ Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shadshere/Track-Apply.git
   cd Track-Apply
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

## Alternative Deployment Methods

### Deploy to Railway

1. **Fork the repository** on GitHub
2. **Visit [railway.app](https://railway.app)**
3. **Connect your GitHub account**
4. **Select "Deploy from GitHub repo"**
5. **Choose your forked TrackApply repository**
6. **Set environment variables:**
   - `SECRET_KEY`: Generate a random secret key
   - `FLASK_ENV`: `production`
7. **Deploy** - Railway will automatically detect it's a Python app

### Deploy to Render

1. **Fork the repository** on GitHub
2. **Visit [render.com](https://render.com)**
3. **Create a new Web Service**
4. **Connect your GitHub repository**
5. **Configuration:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
6. **Set environment variables:**
   - `SECRET_KEY`: Generate a random secret key
   - `FLASK_ENV`: `production`
7. **Deploy**

### Deploy to PythonAnywhere

1. **Create account** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload your code** via Files tab
3. **Create a web app:**
   - Choose "Manual configuration"
   - Select Python 3.x
4. **Configure WSGI file:**
   ```python
   import sys
   path = '/home/yourusername/Track-Apply'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app import app as application
   ```
5. **Install requirements** in Bash console:
   ```bash
   pip3.x install --user -r requirements.txt
   ```
6. **Reload web app**
