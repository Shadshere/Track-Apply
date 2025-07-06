from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Database configuration
print(f"Environment check - PORT: {os.environ.get('PORT')}")
print(f"Environment check - RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT')}")
print(f"Environment check - DYNO: {os.environ.get('DYNO')}")
print(f"Environment check - RENDER: {os.environ.get('RENDER')}")

# Try different database paths for Railway
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Try Railway's data directory first, fallback to tmp
    DATABASE = os.environ.get('DATABASE_PATH', './trackApply.db')
elif os.environ.get('PORT') or os.environ.get('DYNO') or os.environ.get('RENDER'):
    DATABASE = '/tmp/trackApply.db'
else:
    DATABASE = 'trackApply.db'

print(f"Using database path: {DATABASE}")

def get_db_connection():
    """Get database connection with proper timeout and WAL mode"""
    try:
        conn = sqlite3.connect(DATABASE, timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode for better concurrency
        conn.execute('PRAGMA journal_mode=WAL;')
        # Set busy timeout
        conn.execute('PRAGMA busy_timeout=30000;')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize the database with required tables"""
    try:
        print(f"Initializing database at: {DATABASE}")
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
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise

def add_sample_data():
    """Add sample data for testing on cloud platforms"""
    try:
        conn = get_db_connection()
        
        # Check if we already have data
        count = conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()
        if count['count'] > 0:
            print("Sample data already exists")
            conn.close()
            return
            
        # Add sample applications
        sample_apps = [
            ('Google', 'Software Engineer', '2025-07-01', 'Applied', 'Applied through careers page'),
            ('Microsoft', 'Frontend Developer', '2025-07-02', 'Interview', 'Phone screening completed'),
            ('Apple', 'iOS Developer', '2025-07-03', 'Under Review', 'Waiting for technical interview'),
        ]
        
        for app in sample_apps:
            conn.execute('''
                INSERT INTO applications (company_name, job_title, application_date, status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', app)
        
        conn.commit()
        conn.close()
        print("Sample data added successfully")
    except Exception as e:
        print(f"Error adding sample data: {e}")

# Initialize database when app starts
with app.app_context():
    try:
        init_db()
        print("Database initialized in app context")
        
        # Add sample data on cloud platforms for testing
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
            add_sample_data()
            
    except Exception as e:
        print(f"Failed to initialize database in app context: {e}")
    try:
        add_sample_data()
    except Exception as e:
        print(f"Failed to add sample data in app context: {e}")

@app.route('/')
def index():
    """Home page showing all applications"""
    conn = None
    try:
        print(f"Index route: connecting to database {DATABASE}")
        conn = get_db_connection()
        
        # Check total count first
        count_result = conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()
        print(f"Index route: Total applications in database: {count_result['count']}")
        
        applications = conn.execute('''
            SELECT * FROM applications 
            ORDER BY application_date DESC, created_at DESC
        ''').fetchall()
        
        print(f"Index route: Retrieved {len(applications)} applications")
        for app in applications:
            print(f"Application: ID={app['id']}, Company={app['company_name']}, Job={app['job_title']}")
        
        # Count applications by status
        status_counts = conn.execute('''
            SELECT status, COUNT(*) as count 
            FROM applications 
            GROUP BY status
        ''').fetchall()
        
        print(f"Index route: Status counts: {[(row['status'], row['count']) for row in status_counts]}")
        
        stats = {row['status']: row['count'] for row in status_counts}
        
        print(f"Index route: Final stats dict: {stats}")
        print(f"Index route: Rendering template with {len(applications)} applications")
        
        return render_template('index.html', applications=applications, stats=stats)
    except Exception as e:
        print(f"Error in index route: {e}")
        # If database doesn't exist, initialize it and return empty page
        try:
            init_db()
            return render_template('index.html', applications=[], stats={})
        except Exception as init_error:
            print(f"Failed to initialize database in index route: {init_error}")
            return f"Database Error: {init_error}", 500
    finally:
        if conn:
            conn.close()

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    """Add new job application"""
    if request.method == 'POST':
        company_name = request.form['company_name']
        job_title = request.form['job_title']
        application_date = request.form['application_date']
        status = request.form['status']
        notes = request.form['notes']
        
        print(f"Received form data: {company_name}, {job_title}, {application_date}, {status}")
        
        if not company_name or not job_title or not application_date:
            flash('Company name, job title, and application date are required!', 'error')
            return render_template('add.html')
        
        conn = None
        try:
            conn = get_db_connection()
            print(f"Inserting into database: {DATABASE}")
            
            cursor = conn.execute('''
                INSERT INTO applications (company_name, job_title, application_date, status, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (company_name, job_title, application_date, status, notes))
            
            print(f"Inserted record with ID: {cursor.lastrowid}")
            conn.commit()
            
            # Verify the insertion
            count = conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()
            print(f"Total applications in database: {count['count']}")
            
            flash('Application added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error adding application: {e}")
            flash('Error adding application. Please try again.', 'error')
            return render_template('add.html')
        finally:
            if conn:
                conn.close()
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    """Edit existing job application"""
    conn = None
    try:
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
            
            flash('Application updated successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('edit.html', application=application)
    except Exception as e:
        print(f"Error in edit route: {e}")
        flash('Error accessing application. Please try again.', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/delete/<int:id>')
def delete_application(id):
    """Delete job application"""
    conn = None
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM applications WHERE id = ?', (id,))
        conn.commit()
        flash('Application deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting application: {e}")
        flash('Error deleting application. Please try again.', 'error')
    finally:
        if conn:
            conn.close()
    
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

@app.route('/debug')
def debug_database():
    """Debug route to check database contents"""
    conn = None
    try:
        conn = get_db_connection()
        
        # Check if table exists
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        # Get all applications
        applications = conn.execute('SELECT * FROM applications ORDER BY created_at DESC').fetchall()
        
        # Count total
        count = conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()
        
        debug_info = {
            'database_path': DATABASE,
            'tables': [table['name'] for table in tables],
            'total_applications': count['count'],
            'applications': [dict(app) for app in applications]
        }
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Print environment info for debugging
    print(f"DATABASE path: {DATABASE}")
    print(f"PORT env var: {os.environ.get('PORT')}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Initialize database on first run
    init_db()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Starting app on port {port}, debug={debug}")
    app.run(debug=debug, host='0.0.0.0', port=port)
