#!/usr/bin/env python3
"""
Download job data from Adzuna API and save to JSON format for database ingestion.
"""

import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def search_jobs_adzuna(role: str, location: str, num_results: int = 10) -> list:
    """
    Search for jobs using Adzuna API.
    
    Args:
        role: Job title or role to search for
        location: Geographic location for job search
        num_results: Number of job results to return (default: 10)
    
    Returns:
        List of job dictionaries
    """
    # Check if required environment variables are loaded
    required_vars = ['ADZUNA_APP_ID', 'ADZUNA_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("📝 Add these to your .env file:")
        print("ADZUNA_APP_ID=your_adzuna_app_id_here")
        print("ADZUNA_API_KEY=your_adzuna_api_key_here")
        return []
    
    app_id = os.getenv('ADZUNA_APP_ID')
    api_key = os.getenv('ADZUNA_API_KEY')
    
    base_url = "http://api.adzuna.com/v1/api/jobs"
    url = f"{base_url}/us/search/1"
    
    params = {
        'app_id': app_id,
        'app_key': api_key,
        'results_per_page': num_results,
        'what': role,
        'where': location,
        'content-type': 'application/json'
    }
    
    try:
        print(f"🔍 Searching for '{role}' jobs in '{location}'...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        jobs_data = response.json()

        job_listings = []
        for job in jobs_data.get('results', []):
            # Extract and clean job data
            job_details = {
                'title': job.get('title', 'N/A'),
                'company': job.get('company', {}).get('display_name', 'N/A'),
                'location': job.get('location', {}).get('display_name', 'N/A'),
                'salary_min': job.get('salary_min'),
                'salary_max': job.get('salary_max'),
                'salary_currency': 'USD',  # Adzuna returns USD for US jobs
                'employment_type': 'Full-time',  # Default assumption
                'experience_level': 'Mid-level',  # Default assumption
                'skills': extract_skills_from_description(job.get('description', '')),
                'description': job.get('description', 'No description available'),
                'posted_date': job.get('created', datetime.now().strftime('%Y-%m-%d')),
                'application_url': job.get('redirect_url', 'N/A'),
                'remote_ok': 1 if 'remote' in job.get('title', '').lower() or 'remote' in job.get('description', '').lower() else 0
            }
            job_listings.append(job_details)
        
        print(f"✅ Found {len(job_listings)} jobs from Adzuna API")
        return job_listings
        
    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error: {err}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []

def extract_skills_from_description(description: str) -> str:
    """
    Extract common technical skills from job description.
    This is a simple keyword extraction - could be enhanced with NLP.
    """
    if not description:
        return ""
    
    # Common technical skills to look for
    skills_keywords = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'React', 'Angular', 'Vue',
        'Node.js', 'Django', 'Flask', 'Spring', 'Express', 'SQL', 'PostgreSQL',
        'MongoDB', 'Redis', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
        'Git', 'Linux', 'REST', 'GraphQL', 'Microservices', 'CI/CD',
        'Machine Learning', 'AI', 'Data Science', 'TensorFlow', 'PyTorch',
        'Pandas', 'NumPy', 'Scikit-learn', 'HTML', 'CSS', 'Bootstrap',
        'jQuery', 'Webpack', 'Babel', 'Jest', 'Mocha', 'Selenium'
    ]
    
    found_skills = []
    description_lower = description.lower()
    
    for skill in skills_keywords:
        if skill.lower() in description_lower:
            found_skills.append(skill)
    
    return ', '.join(found_skills[:10])  # Limit to 10 skills

def save_jobs_to_json(jobs: list, filename: str = "adzuna_jobs.json"):
    """Save job listings to JSON file for database ingestion."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(jobs)} jobs to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving jobs to file: {e}")
        return False

def main():
    """Main function to download jobs from Adzuna API."""
    print("🚀 Adzuna Job Downloader")
    print("=" * 40)
    
    # Configuration - you can modify these parameters
    # Note: Adzuna API is configured for US market, so we'll search US locations
    # but include companies that have Indian operations
    search_queries = [
        {"role": "Software Engineer", "location": "San Francisco", "num_results": 8},
        {"role": "Software Engineer", "location": "New York", "num_results": 7},
        {"role": "Python Developer", "location": "Seattle", "num_results": 8},
        {"role": "Python Developer", "location": "Austin", "num_results": 7},
        {"role": "React Developer", "location": "Remote", "num_results": 10},
        {"role": "Data Scientist", "location": "Boston", "num_results": 8},
        {"role": "Data Scientist", "location": "Chicago", "num_results": 7},
        {"role": "DevOps Engineer", "location": "Denver", "num_results": 8},
        {"role": "DevOps Engineer", "location": "Portland", "num_results": 7}
    ]
    
    all_jobs = []
    
    for query in search_queries:
        print(f"\n🔍 Searching: {query['role']} in {query['location']}")
        jobs = search_jobs_adzuna(
            role=query['role'],
            location=query['location'],
            num_results=query['num_results']
        )
        all_jobs.extend(jobs)
    
    if all_jobs:
        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            key = (job['title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        print(f"\n📊 Total unique jobs found: {len(unique_jobs)}")
        
        # Save to JSON file
        if save_jobs_to_json(unique_jobs, "adzuna_jobs.json"):
            print("✅ Jobs saved successfully!")
            print("💡 Next step: Run 'python ingest_jobs_from_json.py' to load into database")
        else:
            print("❌ Failed to save jobs")
    else:
        print("❌ No jobs found. Check your API credentials and try again.")

if __name__ == "__main__":
    main()
