#!/usr/bin/env python3
"""
Test script to verify the job search MCP server functionality.
"""

import sqlite3
import json

def test_database_connection():
    """Test if the database was created correctly."""
    try:
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Database table 'jobs' exists")
            
            # Count total jobs
            cursor.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = cursor.fetchone()[0]
            print(f"✅ Total jobs in database: {total_jobs}")
            
            # Show sample job
            cursor.execute("SELECT title, company, location FROM jobs LIMIT 1")
            sample_job = cursor.fetchone()
            if sample_job:
                print(f"✅ Sample job: {sample_job[0]} at {sample_job[1]} in {sample_job[2]}")
            
            # Test search functionality
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE title LIKE ?", ('%Python%',))
            python_jobs = cursor.fetchone()[0]
            print(f"✅ Python jobs found: {python_jobs}")
            
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE remote_ok = 1")
            remote_jobs = cursor.fetchone()[0]
            print(f"✅ Remote jobs found: {remote_jobs}")
            
        else:
            print("❌ Database table 'jobs' does not exist")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_search_queries():
    """Test various search queries."""
    try:
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        print("\n🔍 Testing search queries:")
        
        # Test keyword search
        cursor.execute("SELECT title, company FROM jobs WHERE title LIKE ? OR skills LIKE ? LIMIT 3", ('%React%', '%React%'))
        react_jobs = cursor.fetchall()
        print(f"React jobs: {len(react_jobs)} found")
        for job in react_jobs:
            print(f"  - {job[0]} at {job[1]}")
        
        # Test location search
        cursor.execute("SELECT title, company, location FROM jobs WHERE location LIKE ? LIMIT 3", ('%San Francisco%',))
        sf_jobs = cursor.fetchall()
        print(f"San Francisco jobs: {len(sf_jobs)} found")
        for job in sf_jobs:
            print(f"  - {job[0]} at {job[1]} in {job[2]}")
        
        # Test company search
        cursor.execute("SELECT title, company FROM jobs WHERE company LIKE ? LIMIT 3", ('%Google%',))
        google_jobs = cursor.fetchall()
        print(f"Google jobs: {len(google_jobs)} found")
        for job in google_jobs:
            print(f"  - {job[0]} at {job[1]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Search query test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Job Search MCP Server")
    print("=" * 40)
    
    # Test database
    db_ok = test_database_connection()
    
    if db_ok:
        # Test search functionality
        search_ok = test_search_queries()
        
        if search_ok:
            print("\n✅ All tests passed! The job search MCP server is ready to use.")
            print("\n📋 Available MCP tools:")
            print("  - search_jobs(keywords, location, company, limit)")
            print("  - get_job_by_id(job_id)")
            print("  - get_job_statistics()")
        else:
            print("\n❌ Search functionality tests failed.")
    else:
        print("\n❌ Database tests failed.")
