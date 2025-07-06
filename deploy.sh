#!/bin/bash
# TrackApply Deployment Script

echo "🚀 Preparing TrackApply for deployment..."

# Add deployment files to git
git add Procfile requirements.txt app.py

# Commit changes
git commit -m "Add production deployment configuration

- Add Procfile for Gunicorn deployment
- Update requirements.txt with gunicorn
- Configure app.py for production environment variables
- Auto-initialize database on startup"

# Push to GitHub (required for cloud deployments)
git push origin main

echo "✅ Ready for deployment!"
echo ""
echo "🌐 Deployment Options:"
echo "1. Railway: https://railway.app"
echo "   - Connect your GitHub repo"
echo "   - Auto-deploys on push"
echo ""
echo "2. Render: https://render.com"
echo "   - Connect GitHub repo"
echo "   - Choose 'Web Service'"
echo ""
echo "3. Heroku: https://heroku.com"
echo "   - heroku create your-app-name"
echo "   - git push heroku main"
echo ""
echo "Your app is ready to deploy! 🎉"
