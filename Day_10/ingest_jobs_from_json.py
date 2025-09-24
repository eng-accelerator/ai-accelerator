#!/usr/bin/env python3
"""
Script to ingest job data from JSON file (from Adzuna API) into SQLite database.
"""

import sqlite3
import json
import os
from datetime import datetime

def create_jobs_database():
    """Create the jobs database and table."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    # Drop existing table
    cursor.execute("DROP TABLE IF EXISTS `jobs`")
    
    # Create jobs table
    query_create = """
    CREATE TABLE IF NOT EXISTS `jobs` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `title` TEXT NOT NULL,
        `company` TEXT NOT NULL,
        `location` TEXT NOT NULL,
        `salary_min` INTEGER,
        `salary_max` INTEGER,
        `salary_currency` TEXT DEFAULT 'USD',
        `employment_type` TEXT,
        `experience_level` TEXT,
        `skills` TEXT,
        `description` TEXT,
        `posted_date` TEXT,
        `application_url` TEXT,
        `remote_ok` INTEGER DEFAULT 0
    );
    """
    
    cursor.execute(query_create)
    conn.commit()
    return conn, cursor

def ingest_jobs_from_json(json_file='adzuna_jobs.json'):
    """Read jobs from JSON file and insert into database."""
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        print("💡 Run 'python download_jobs_adzuna.py' first to fetch jobs from Adzuna API")
        return False
    
    try:
        # Read JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)
        
        print(f"📄 Found {len(jobs_data)} jobs in {json_file}")
        
        # Create database
        conn, cursor = create_jobs_database()
        
        # Insert jobs
        inserted_count = 0
        for job in jobs_data:
            try:
                data = [
                    job.get('title', 'N/A'),
                    job.get('company', 'N/A'),
                    job.get('location', 'N/A'),
                    job.get('salary_min'),
                    job.get('salary_max'),
                    job.get('salary_currency', 'USD'),
                    job.get('employment_type', 'Full-time'),
                    job.get('experience_level', 'Mid-level'),
                    job.get('skills', ''),
                    job.get('description', ''),
                    job.get('posted_date', datetime.now().strftime('%Y-%m-%d')),
                    job.get('application_url', ''),
                    job.get('remote_ok', 0)
                ]
                
                cursor.execute("""
                    INSERT INTO `jobs` (
                        `title`, `company`, `location`, `salary_min`, `salary_max`, 
                        `salary_currency`, `employment_type`, `experience_level`, 
                        `skills`, `description`, `posted_date`, `application_url`, `remote_ok`
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
                inserted_count += 1
                
            except Exception as e:
                print(f"⚠️  Error inserting job '{job.get('title', 'Unknown')}': {e}")
                continue
        
        conn.commit()
        conn.close()
        print(f"✅ Successfully ingested {inserted_count} jobs into the database!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def verify_database():
    """Verify the database was created correctly."""
    try:
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()
        
        # Count total jobs
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]
        print(f"📊 Total jobs in database: {total_jobs}")
        
        # Show sample jobs
        cursor.execute("SELECT title, company, location FROM jobs LIMIT 3")
        sample_jobs = cursor.fetchall()
        print("\n📋 Sample jobs:")
        for i, job in enumerate(sample_jobs, 1):
            print(f"  {i}. {job[0]} at {job[1]} in {job[2]}")
        
        # Count by location
        cursor.execute("SELECT location, COUNT(*) FROM jobs GROUP BY location ORDER BY COUNT(*) DESC LIMIT 5")
        location_stats = cursor.fetchall()
        print("\n📍 Top locations:")
        for location, count in location_stats:
            print(f"  - {location}: {count} jobs")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

if __name__ == "__main__":
    print("🗄️  Job Database Ingestion from Adzuna JSON")
    print("=" * 50)
    
    # Ingest jobs from JSON
    success = ingest_jobs_from_json()
    
    if success:
        print("\n🔍 Verifying database...")
        verify_database()
        print("\n✅ Database setup complete!")
        print("💡 You can now use the MCP server to search jobs")
    else:
        print("\n❌ Database setup failed")
