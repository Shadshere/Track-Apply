# TrackApply - Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
TrackApply is a Flask-based web application for tracking job applications. It helps job seekers stay organized during their job search by allowing them to log and monitor all their job applications in one place.

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Styling**: Custom CSS with gradients and modern design

## Key Features
- Add, edit, and delete job applications
- Track application status (Applied, Under Review, Interview, Offer, Rejected)
- Dashboard with statistics
- Mobile-friendly responsive design
- Modern UI with gradients and animations

## Code Guidelines
- Follow Flask best practices
- Use SQLite with proper connection handling
- Implement form validation both client-side and server-side
- Use Bootstrap 5 components for consistent UI
- Apply custom CSS for modern gradients and animations
- Ensure mobile responsiveness
- Use semantic HTML and accessible design

## Database Schema
The main table is `applications` with fields:
- id (Primary Key)
- company_name (Required)
- job_title (Required)
- application_date (Required)
- status (Default: 'Applied')
- notes (Optional)
- created_at, updated_at (Timestamps)

## File Structure
- `app.py` - Main Flask application
- `templates/` - Jinja2 templates
- `static/css/` - Custom CSS files
- `static/js/` - JavaScript files
- `static/images/` - Image assets including logo
- `requirements.txt` - Python dependencies

## Design Principles
- Modern, clean design with gradients
- Interactive elements with hover effects
- Consistent color scheme with primary gradient (blue to purple)
- Responsive design for mobile and desktop
- Accessible UI with proper ARIA labels and semantic HTML
