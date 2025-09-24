# Job Search MCP Server

A Model Context Protocol (MCP) server that provides AI-powered job search capabilities through Claude Desktop. This server integrates with the Adzuna API to fetch real-time job listings and allows you to search for software engineering positions with advanced filtering.

## Features

- 🔍 **Smart Job Search**: Search jobs by keywords, location, company, and more
- 📊 **Job Statistics**: Get insights about available positions and market trends
- 🎯 **Detailed Job Info**: Access comprehensive job details including salary, skills, and descriptions
- 🌐 **Real-time Data**: Fetches live job listings from Adzuna API
- 🤖 **AI Integration**: Works seamlessly with Claude Desktop for conversational job search

## Prerequisites

- Python 3.13+
- Adzuna API credentials (free at [developer.adzuna.com](https://developer.adzuna.com/))
- Claude Desktop installed

## Installation

### 1. Install UV (Package Manager)

**On Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**On macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup Project

**Option A: Use the working directory (Recommended)**
```bash
cd ~/job_search_mcp
```

**Option B: Clone and setup from scratch**
```bash
git clone https://github.com/ThomasJanssen-tech/MCP_Server
cd MCP_Server
```

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
# Adzuna API Configuration
ADZUNA_APP_ID=your_adzuna_app_id_here
ADZUNA_API_KEY=your_adzuna_api_key_here
```

Get your free API credentials at [developer.adzuna.com](https://developer.adzuna.com/)

### 4. Install Dependencies

```bash
uv run mcp install main.py
```

## Usage

### Initial Setup (One-time)

1. **Download Job Data:**
   ```bash
   uv run download_jobs_adzuna.py
   ```

2. **Load Data into Database:**
   ```bash
   uv run ingest_jobs_from_json.py
   ```

### Using with Claude Desktop

Once installed, you can ask Claude Desktop questions like:

- "Find me Python developer jobs in San Francisco"
- "Show me remote software engineering positions"
- "What are the top companies hiring right now?"
- "Get me job statistics"
- "Search for React developer jobs with salary over $100k"

## Available MCP Tools

### 1. `search_jobs(keywords, location, company, limit)`
Search for jobs with flexible filtering options.

**Parameters:**
- `keywords`: Job title or skills to search for (e.g., "python developer", "react")
- `location`: Location to search in (e.g., "San Francisco", "Remote")
- `company`: Company name to filter by
- `limit`: Maximum number of results (default: 10)

**Example:**
```python
search_jobs(keywords="python developer", location="San Francisco", limit=5)
```

### 2. `get_job_by_id(job_id)`
Get detailed information about a specific job by its ID.

**Parameters:**
- `job_id`: The unique ID of the job

**Example:**
```python
get_job_by_id(job_id=1)
```

### 3. `get_job_statistics()`
Get statistics about available jobs including:
- Total job count
- Remote job count
- Top locations
- Top companies

**Example:**
```python
get_job_statistics()
```

## File Structure

```
job_search_mcp/                    # Working directory: ~/job_search_mcp
├── main.py                        # 🎯 Main MCP server with job search tools
├── download_jobs_adzuna.py        # 🔍 Script to fetch jobs from Adzuna API
├── ingest_jobs_from_json.py       # 🗄️ Script to load jobs into SQLite database
├── test_job_search.py             # 🧪 Test script to verify functionality
├── jobs.db                        # 📊 SQLite database with job listings
├── adzuna_jobs.json              # 📄 Raw job data from Adzuna API
├── .env                          # 🔐 Environment variables (API keys)
├── pyproject.toml                # ⚙️ Python project configuration
├── README.md                     # 📖 This file
└── uv.lock                       # 🔒 Package lock file
```

## Updating Job Data

To refresh the job database with new listings:

```bash
# Fetch new jobs from Adzuna API
uv run download_jobs_adzuna.py

# Load new data into database
uv run ingest_jobs_from_json.py
```

## Testing

Run the test script to verify everything is working:

```bash
uv run test_job_search.py
```

## Customization

### Adding New Job Search Queries

Edit `download_jobs_adzuna.py` to modify the search queries:

```python
search_queries = [
    {"role": "Software Engineer", "location": "San Francisco", "num_results": 10},
    {"role": "Python Developer", "location": "New York", "num_results": 10},
    {"role": "React Developer", "location": "Remote", "num_results": 10},
    {"role": "Data Scientist", "location": "Seattle", "num_results": 10},
    {"role": "DevOps Engineer", "location": "Austin", "num_results": 10}
    # Add your custom searches here
]
```

### Modifying Database Schema

The job database schema is defined in `ingest_jobs_from_json.py`. You can add new fields by:

1. Modifying the SQL table creation query
2. Updating the data insertion logic
3. Adding new fields to the MCP tools in `main.py`

## Troubleshooting

### Common Issues

1. **"Missing environment variables" error:**
   - Ensure your `.env` file exists and contains valid Adzuna API credentials
   - Check that the file is in the same directory as `main.py`

2. **"No jobs found" error:**
   - Verify your Adzuna API credentials are correct
   - Check your internet connection
   - Try different search terms or locations

3. **Database connection issues:**
   - Ensure `jobs.db` file exists (run `ingest_jobs_from_json.py` first)
   - Check file permissions

4. **Permission errors on macOS:**
   - If you encounter permission errors, the project has been moved to `~/job_search_mcp`
   - Use the working directory: `cd ~/job_search_mcp`

### Getting Help

- Check the [MCP Python SDK documentation](https://github.com/modelcontextprotocol/python-sdk)
- Visit [Adzuna API documentation](https://developer.adzuna.com/docs)
- Review the test output for debugging information

## Current Database Status

- **35 real job listings** from Adzuna API
- **Multiple locations**: San Francisco, New York, Seattle, Austin
- **Various roles**: Software Engineer, Python Developer, Data Scientist, DevOps Engineer
- **Remote positions** available
- **Skills extraction** from job descriptions

## Quick Start

1. **Navigate to working directory:**
   ```bash
   cd ~/job_search_mcp
   ```

2. **Install MCP server:**
   ```bash
   uv run mcp install main.py
   ```

3. **Open Claude Desktop and start searching:**
   - "Find me Python developer jobs"
   - "Show me remote positions"
   - "Get job statistics"

## License

This project is based on the original MCP Server template. See the original repository for licensing information.

## Contributing

Feel free to submit issues and enhancement requests! This is a great starting point for building more sophisticated job search applications.