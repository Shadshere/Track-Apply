from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE = 'trackApply.db'

def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize the database with required tables"""
    try:
        logger.info("Initializing database...")
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                application_date DATE NOT NULL,
                status TEXT NOT NULL DEFAULT 'Applied',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

@app.route('/')
def index():
    """Home page showing all applications"""
    conn = get_db_connection()
    applications = conn.execute('''
        SELECT * FROM applications 
        ORDER BY application_date DESC, created_at DESC
    ''').fetchall()
    conn.close()
    
    # Count applications by status
    conn = get_db_connection()
    status_counts = conn.execute('''
        SELECT status, COUNT(*) as count 
        FROM applications 
        GROUP BY status
    ''').fetchall()
    conn.close()
    
    stats = {row['status']: row['count'] for row in status_counts}
    
    return render_template('index.html', applications=applications, stats=stats)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    """Add new job application"""
    if request.method == 'POST':
        try:
            company_name = request.form['company_name']
            job_title = request.form['job_title']
            application_date = request.form['application_date']
            status = request.form['status']
            notes = request.form['notes']
            
            logger.info(f"Adding application: {company_name} - {job_title}")
            
            if not company_name or not job_title or not application_date:
                flash('Company name, job title, and application date are required!', 'error')
                return render_template('add.html')
            
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO applications (company_name, job_title, application_date, status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (company_name, job_title, application_date, status, notes))
            conn.commit()
            conn.close()
            
            logger.info("Application added successfully")
            flash('Application added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            logger.error(f"Error adding application: {e}")
            flash('An error occurred while adding the application. Please try again.', 'error')
            return render_template('add.html')
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    """Edit existing job application"""
    conn = get_db_connection()
    application = conn.execute('SELECT * FROM applications WHERE id = ?', (id,)).fetchone()
    
    if not application:
        flash('Application not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        application_date = request.form['application_date']
        status = request.form['status']
        notes = request.form['notes']
        
        if not company_name or not job_title or not application_date:
            flash('Company name, job title, and application date are required!', 'error')
            return render_template('edit.html', application=application)
        
        conn.execute('''
            UPDATE applications 
            SET company_name=?, job_title=?, application_date=?, status=?, notes=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (company_name, job_title, application_date, status, notes, id))
        conn.commit()
        conn.close()
        
        flash('Application updated successfully!', 'success')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', application=application)

@app.route('/delete/<int:id>')
def delete_application(id):
    """Delete job application"""
    conn = get_db_connection()
    conn.execute('DELETE FROM applications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/stats')
def api_stats():
    """API endpoint for application statistics"""
    conn = get_db_connection()
    
    # Total applications
    total = conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()['count']
    
    # Applications by status
    status_counts = conn.execute('''
        SELECT status, COUNT(*) as count 
        FROM applications 
        GROUP BY status
    ''').fetchall()
    
    # Recent applications (last 30 days)
    recent = conn.execute('''
        SELECT COUNT(*) as count 
        FROM applications 
        WHERE application_date >= date('now', '-30 days')
    ''').fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total': total,
        'recent': recent,
        'by_status': {row['status']: row['count'] for row in status_counts}
    })

@app.route('/init-db')
def init_database():
    """Manually initialize database - for debugging"""
    try:
        init_db()
        return "Database initialized successfully!"
    except Exception as e:
        logger.error(f"Manual database initialization failed: {e}")
        return f"Database initialization failed: {e}", 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.execute('SELECT 1').fetchone()
        conn.close()
        return "OK", 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return f"Health check failed: {e}", 500

if __name__ == '__main__':
    # Initialize database on first run
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
else:
    # When running with gunicorn, initialize database
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database in gunicorn mode: {e}")
