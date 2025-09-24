from dotenv import load_dotenv
import os
import sqlite3
from mcp.server.fastmcp import FastMCP

load_dotenv()


# Create an MCP server
mcp = FastMCP("JobSearchServer")



@mcp.tool()
def search_jobs(keywords: str = "", location: str = "", company: str = "", limit: int = 10) -> dict:
    """
    Search for software engineer jobs based on keywords, location, and company.
    
    Args:
        keywords: Job title or skills to search for (e.g., "python developer", "react")
        location: Location to search in (e.g., "San Francisco", "Remote")
        company: Company name to filter by
        limit: Maximum number of results to return (default: 10)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "jobs.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build dynamic query based on provided parameters
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    
    if keywords:
        query += " AND (title LIKE ? OR description LIKE ? OR skills LIKE ?)"
        keyword_param = f"%{keywords}%"
        params.extend([keyword_param, keyword_param, keyword_param])
    
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    
    if company:
        query += " AND company LIKE ?"
        params.append(f"%{company}%")
    
    query += " ORDER BY posted_date DESC LIMIT ?"
    params.append(limit)

    result = cursor.execute(query, params)
    jobs = result.fetchall()

    conn.close()

    if jobs:
        job_list = []
        for job in jobs:
            job_data = {
                "id": job[0],
                "title": job[1],
                "company": job[2],
                "location": job[3],
                "salary_min": job[4],
                "salary_max": job[5],
                "salary_currency": job[6],
                "employment_type": job[7],
                "experience_level": job[8],
                "skills": job[9],
                "description": job[10],
                "posted_date": job[11],
                "application_url": job[12],
                "remote_ok": job[13]
            }
            job_list.append(job_data)
        
        return {
            "total_results": len(job_list),
            "jobs": job_list
        }
    else:
        return {"error": "No jobs found matching your criteria."}


@mcp.tool()
def get_job_by_id(job_id: int) -> dict:
    """
    Get detailed information about a specific job by its ID.
    
    Args:
        job_id: The unique ID of the job
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "jobs.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    result = cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = result.fetchone()

    conn.close()

    if job:
        return {
            "id": job[0],
            "title": job[1],
            "company": job[2],
            "location": job[3],
            "salary_min": job[4],
            "salary_max": job[5],
            "salary_currency": job[6],
            "employment_type": job[7],
            "experience_level": job[8],
            "skills": job[9],
            "description": job[10],
            "posted_date": job[11],
            "application_url": job[12],
            "remote_ok": job[13]
        }
    else:
        return {"error": f"No job found with ID {job_id}."}


@mcp.tool()
def get_job_statistics() -> dict:
    """
    Get statistics about available jobs in the database.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "jobs.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total job count
    total_jobs = cursor.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    
    # Get jobs by location
    location_stats = cursor.execute("""
        SELECT location, COUNT(*) as count 
        FROM jobs 
        GROUP BY location 
        ORDER BY count DESC 
        LIMIT 10
    """).fetchall()
    
    # Get jobs by company
    company_stats = cursor.execute("""
        SELECT company, COUNT(*) as count 
        FROM jobs 
        GROUP BY company 
        ORDER BY count DESC 
        LIMIT 10
    """).fetchall()
    
    # Get remote jobs count
    remote_jobs = cursor.execute("SELECT COUNT(*) FROM jobs WHERE remote_ok = 1").fetchone()[0]

    conn.close()

    return {
        "total_jobs": total_jobs,
        "remote_jobs": remote_jobs,
        "top_locations": [{"location": loc[0], "count": loc[1]} for loc in location_stats],
        "top_companies": [{"company": comp[0], "count": comp[1]} for comp in company_stats]
    }
    

if __name__ == "__main__":
    mcp.run()

#    mcp.run(transport="sse", host="127.0.0.1", port=8000)


