"""
Initialize database and add sample data for TrackApply
"""
import sqlite3
from datetime import datetime, timedelta

DATABASE = 'trackApply.db'

def init_with_sample_data():
    """Initialize database with sample applications"""
    conn = sqlite3.connect(DATABASE)
    
    # Create table if it doesn't exist
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
    
    # Check if there's already data
    count = conn.execute('SELECT COUNT(*) FROM applications').fetchone()[0]
    if count > 0:
        print(f"Database already has {count} applications.")
        conn.close()
        return
    
    # Sample data
    sample_apps = [
        {
            'company_name': 'Google',
            'job_title': 'Software Engineer',
            'application_date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'status': 'Under Review',
            'notes': 'Applied through LinkedIn. Great company culture!'
        },
        {
            'company_name': 'Microsoft',
            'job_title': 'Python Developer',
            'application_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'status': 'Interview',
            'notes': 'First round interview scheduled for next week.'
        },
        {
            'company_name': 'Apple',
            'job_title': 'Full Stack Developer',
            'application_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'status': 'Applied',
            'notes': 'Applied through company website.'
        }
    ]
    
    # Insert sample data
    for app in sample_apps:
        conn.execute('''
            INSERT INTO applications (company_name, job_title, application_date, status, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (app['company_name'], app['job_title'], app['application_date'], 
              app['status'], app['notes']))
    
    conn.commit()
    conn.close()
    print("Database initialized with sample data!")

if __name__ == '__main__':
    init_with_sample_data()
