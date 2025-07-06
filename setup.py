#!/usr/bin/env python3
"""
Setup script for TrackApply
"""
import os
import sqlite3

def setup_trackapply():
    """Setup TrackApply application"""
    print("🚀 Setting up TrackApply...")
    
    # Create database
    database = 'trackApply.db'
    conn = sqlite3.connect(database)
    
    # Create table
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
    
    print("✅ Database created successfully!")
    print("✅ Tables created successfully!")
    print("\n🎉 TrackApply setup complete!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nThen open your browser to: http://localhost:5000")

if __name__ == '__main__':
    setup_trackapply()
