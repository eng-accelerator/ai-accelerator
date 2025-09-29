#!/usr/bin/env python3
"""
Enhanced CrewAI Job Search Agent System with Resume Analysis
A comprehensive AI-powered job search automation system that analyzes your resume 
for personalized recommendations using CrewAI framework.

Required .env file format:
OPENAI_API_KEY=your_openai_api_key_here
ADZUNA_APP_ID=your_adzuna_app_id_here  
ADZUNA_API_KEY=your_adzuna_api_key_here

Installation:
pip install crewai langchain langchain-openai requests python-dotenv PyPDF2 pdfplumber
"""

import json
import requests
import os
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai.tools import tool
from crewai.tasks.task_output import TaskOutput
import PyPDF2
import pdfplumber

# Load environment variables from .env file
load_dotenv()


@tool("Resume Parser Tool")
def parse_resume(file_path: str) -> str:
    """
    Parse resume PDF and extract text content.
    
    Args:
        file_path: Path to the resume PDF file
    
    Returns
        Extracted text content from the resume
    """
    if not os.path.exists(file_path):
        return f"Error: Resume file not found at {file_path}. Please check the file path."
    
    try:
        # Try using pdfplumber first (better text extraction)
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():
                return f"✅ Resume parsed successfully!\n\nResume Content:\n{text}"
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2...")
    
    try:
        # Fallback to PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if text.strip():
                return f"✅ Resume parsed successfully!\n\nResume Content:\n{text}"
            else:
                return "Error: Could not extract text from PDF. The file might be image-based or corrupted."
    
    except Exception as e:
        return f"Error: Failed to parse resume PDF. {str(e)}"


@tool("Job Search Tool")
def search_jobs(input_json: str) -> str:
    """
    Search for job listings using the Adzuna API.
    
    Args:
        input_json: JSON string with schema {'role': '<role>', 'location': '<location>', 'num_results': <number>}
    
    Returns:
        Formatted string of job listings
    """
    try:
        # Check if required environment variables are loaded
        required_vars = ['OPENAI_API_KEY', 'ADZUNA_APP_ID', 'ADZUNA_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            error_msg = "❌ Missing required environment variables in .env file:\n"
            for var in missing_vars:
                error_msg += f"   - {var}\n"
            error_msg += "\n📝 Create a .env file in your project directory with:\n"
            error_msg += "OPENAI_API_KEY=your_openai_api_key_here\n"
            error_msg += "ADZUNA_APP_ID=your_adzuna_app_id_here\n"
            error_msg += "ADZUNA_API_KEY=your_adzuna_api_key_here"
            return error_msg
        
        input_data = json.loads(input_json)
        role = input_data['role']
        location = input_data['location']
        num_results = input_data.get('num_results', 5)
    except (json.JSONDecodeError, KeyError) as e:
        return """Error: The tool accepts input in JSON format with the 
                following schema: {'role': '<role>', 'location': '<location>', 'num_results': <number>}. 
                Ensure to format the input accordingly."""

    app_id = os.getenv('ADZUNA_APP_ID')
    api_key = os.getenv('ADZUNA_API_KEY')
    
    if not app_id or not api_key:
        return "Error: Please set ADZUNA_APP_ID and ADZUNA_API_KEY in your .env file."
    
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
        response = requests.get(url, params=params)
        response.raise_for_status()
        jobs_data = response.json()

        job_listings = []
        for job in jobs_data.get('results', []):
            job_details = {
                'title': job.get('title', 'N/A'),
                'company': job.get('company', {}).get('display_name', 'N/A'),
                'location': job.get('location', {}).get('display_name', 'N/A'),
                'salary': job.get('salary_min', 'Not specified'),
                'description': job.get('description', '')[:300] + '...' if job.get('description') else 'No description',
                'url': job.get('redirect_url', 'N/A')
            }
            
            formatted_job = f"""
Title: {job_details['title']}
Company: {job_details['company']}
Location: {job_details['location']}
Salary: {job_details['salary']}
Description: {job_details['description']}
URL: {job_details['url']}
---"""
            job_listings.append(formatted_job)
        
        return '\n'.join(job_listings) if job_listings else "No jobs found for the specified criteria."
        
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error: {err}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


class EnhancedJobSearchAgentSystem:
    """Enhanced Job Search Agent System with Resume Analysis"""
    
    def __init__(self, resume_path: str = None):
        """
        Initialize the Enhanced Job Search Agent System
        
        Args:
            resume_path: Path to the resume PDF file for personalized analysis
        """
        # Verify API key is set from .env file
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("Please set OPENAI_API_KEY in your .env file")
        
        self.llm = ChatOpenAI(model="gpt-4.1-2025-04-14")
        self.resume_path = resume_path
        self.resume_content = ""
        
        # Parse resume if provided
        if resume_path:
            self.parse_resume()
        
        self.setup_agents()
        self.setup_tasks()
        self.setup_crew()
    
    def parse_resume(self):
        """Parse the resume and store content for agent context"""
        if self.resume_path:
            print(f"📄 Parsing resume from: {self.resume_path}")
            # Call the tool function directly
            self.resume_content = self._parse_resume_direct(self.resume_path)
            if "✅ Resume parsed successfully!" in self.resume_content:
                print("✅ Resume parsed and ready for analysis!")
            else:
                print("❌ Resume parsing failed. Proceeding without resume context.")
                self.resume_content = ""
    
    def _parse_resume_direct(self, file_path: str) -> str:
        """Direct resume parsing function without tool decorator"""
        if not os.path.exists(file_path):
            return f"Error: Resume file not found at {file_path}. Please check the file path."
        
        try:
            # Try using pdfplumber first (better text extraction)
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    return f"✅ Resume parsed successfully!\n\nResume Content:\n{text}"
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        try:
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if text.strip():
                    return f"✅ Resume parsed successfully!\n\nResume Content:\n{text}"
                else:
                    return "Error: Could not extract text from PDF. The file might be image-based or corrupted."
        
        except Exception as e:
            return f"Error: Failed to parse resume PDF. {str(e)}"
    
    def callback_function(self, output: TaskOutput):
        """Save task output to file"""
        try:
            with open("task_output.txt", "a", encoding='utf-8') as file:
                file.write(f"=== {output.agent} - {output.description} ===\n")
                file.write(f"{output.result}\n\n")
            print(f"✅ Result saved to task_output.txt")
        except Exception as e:
            print(f"❌ Error saving output: {e}")
    
    def setup_agents(self):
        """Initialize all AI agents with enhanced capabilities"""
        
        resume_context = f"\n\nCandidate's Resume Content:\n{self.resume_content}" if self.resume_content else ""
        
        self.job_searcher_agent = Agent(
            role='Senior Job Search Specialist',
            goal='Find the most relevant job opportunities that match the candidate\'s profile and specified criteria',
            backstory=f"""You are an expert job search specialist with extensive experience in 
            identifying high-quality job opportunities. You excel at understanding both job requirements 
            and candidate profiles to find the perfect matches.{resume_context}""",
            verbose=True,
            llm=self.llm,
            allow_delegation=True,
            tools=[search_jobs]
        )
        
        self.skills_development_agent = Agent(
            role='Personalized Skills Development Advisor',
            goal='Analyze job requirements against the candidate\'s current skills and provide targeted development recommendations',
            backstory=f"""You are a seasoned career development expert who specializes in 
            identifying skill gaps by comparing job requirements with candidate backgrounds. 
            You create personalized learning paths based on individual experience and career goals.{resume_context}""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        self.interview_preparation_coach = Agent(
            role='Personalized Interview Preparation Expert',
            goal='Prepare candidates for interviews by leveraging their specific background and experience',
            backstory=f"""You are a professional interview coach who creates personalized interview 
            strategies. You help candidates highlight their unique strengths and address potential 
            weaknesses based on their specific background and target roles.{resume_context}""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        self.career_advisor = Agent(
            role='Personalized Career Strategy Advisor',
            goal='Provide strategic career advice tailored to the candidate\'s specific background and goals',
            backstory=f"""You are a senior career strategist who creates personalized career 
            advancement plans. You understand how to position candidates based on their unique 
            background, optimize their personal brand, and create targeted networking strategies.{resume_context}""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def setup_tasks(self):
        """Initialize all tasks for the agents with resume context"""
        
        self.job_search_task = Task(
            description="""Search for current job openings based on the specified role and location. 
            Use the Job Search tool with the following parameters:
            - Find 5-10 relevant positions
            - Focus on quality over quantity
            - Include detailed job descriptions and requirements
            - Highlight key qualifications and skills needed
            
            Format your search as JSON: {'role': '<role>', 'location': '<location>', 'num_results': <number>}""",
            expected_output="A formatted list of job openings with titles, companies, locations, salaries, descriptions, and URLs",
            agent=self.job_searcher_agent,
            tools=[search_jobs],
            callback=self.callback_function
        )
        
        self.skills_analysis_task = Task(
            description=f"""Analyze the job openings and create a PERSONALIZED skills assessment:
            
            1. Compare the candidate's current skills (from resume) with job requirements
            2. Identify SPECIFIC skill gaps and strengths
            3. Categorize skills as: Already Have, Need to Improve, Need to Learn
            4. Provide targeted recommendations including:
               - Specific courses/certifications for identified gaps
               - How to better highlight existing skills
               - Timeline for skill development based on current level
               - Which skills to prioritize for maximum impact
            5. Create a personalized learning roadmap
            
            {f'Use the candidate resume content for context: {self.resume_content}' if self.resume_content else 'No resume provided - provide general recommendations.'}""",
            expected_output="A personalized skills gap analysis with specific recommendations tailored to the candidate's background",
            agent=self.skills_development_agent,
            context=[self.job_search_task],
            callback=self.callback_function
        )
        
        self.interview_prep_task = Task(
            description=f"""Create a PERSONALIZED interview preparation strategy:
            
            1. Generate role-specific questions tailored to the candidate's background
            2. Create STAR method examples using the candidate's actual experience
            3. Identify potential interview challenges based on resume gaps or career changes
            4. Provide specific talking points to highlight candidate's unique strengths
            5. Address potential concerns employers might have
            6. Create customized salary negotiation strategy based on experience level
            7. Develop elevator pitch based on candidate's background
            
            {f'Base recommendations on candidate resume: {self.resume_content}' if self.resume_content else 'Provide general interview preparation advice.'}""",
            expected_output="A personalized interview preparation guide with customized questions, answers, and strategies",
            agent=self.interview_preparation_coach,
            context=[self.job_search_task, self.skills_analysis_task],
            callback=self.callback_function
        )
        
        self.career_strategy_task = Task(
            description=f"""Develop a PERSONALIZED career strategy plan:
            
            1. Analyze current resume and suggest specific improvements for target roles
            2. Create LinkedIn optimization strategy based on existing profile content
            3. Identify networking opportunities relevant to candidate's industry/background
            4. Suggest specific portfolio projects based on current skills and target roles
            5. Create personal branding strategy that highlights unique value proposition
            6. Develop application strategy tailored to candidate's experience level
            7. Provide specific action items with timeline for career advancement
            
            {f'Base all recommendations on candidate background: {self.resume_content}' if self.resume_content else 'Provide general career strategy advice.'}""",
            expected_output="A personalized career strategy plan with specific, actionable recommendations",
            agent=self.career_advisor,
            context=[self.job_search_task, self.skills_analysis_task],
            callback=self.callback_function
        )
    
    def setup_crew(self):
        """Initialize the CrewAI crew"""
        self.crew = Crew(
            agents=[
                self.job_searcher_agent,
                self.skills_development_agent,
                self.interview_preparation_coach,
                self.career_advisor
            ],
            tasks=[
                self.job_search_task,
                self.skills_analysis_task,
                self.interview_prep_task,
                self.career_strategy_task
            ],
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True
        )
    
    def search_jobs(self, role: str, location: str, num_results: int = 5):
        """
        Execute the personalized job search process
        
        Args:
            role: Job title or role to search for
            location: Geographic location for job search
            num_results: Number of job results to return (default: 5)
        
        Returns:
            Complete personalized analysis and recommendations from all agents
        """
        print(f"🚀 Starting PERSONALIZED job search for '{role}' in '{location}'...")
        if self.resume_content:
            print("📄 Using resume content for personalized recommendations")
        else:
            print("⚠️  No resume provided - using general recommendations")
            
        print("📝 This process will:")
        print("   1. Search for relevant job openings")
        print("   2. Compare job requirements with your background")
        print("   3. Create personalized skill development plan")
        print("   4. Prepare customized interview strategies")
        print("   5. Generate targeted career optimization plan")
        print("   6. Provide actionable next steps")
        print("\n" + "="*50)
        
        # Clear previous output file
        with open("task_output.txt", "w") as file:
            file.write(f"PERSONALIZED Job Search Analysis Report\n")
            file.write(f"Role: {role}\n")
            file.write(f"Location: {location}\n")
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Resume Analyzed: {'Yes' if self.resume_content else 'No'}\n")
            file.write("="*50 + "\n\n")
        
        # Update the job search task with specific parameters
        search_params = json.dumps({
            'role': role,
            'location': location,
            'num_results': num_results
        })
        
        self.job_search_task.description = f"""Search for current job openings for the {role} role in {location} 
        using the Job Search tool. Find {num_results} relevant positions that would be suitable for the candidate's background.
        Use this exact input: {search_params}"""
        
        try:
            # Execute the crew
            result = self.crew.kickoff()
            
            print("\n" + "="*50)
            print("✅ Personalized job search analysis complete!")
            print("📄 Detailed results saved to 'task_output.txt'")
            if self.resume_content:
                print("🎯 All recommendations are tailored to your specific background!")
            print("="*50)
            
            return result
            
        except Exception as e:
            print(f"❌ Error during job search execution: {e}")
            return None


def main():
    """Main function to run the enhanced job search system"""
    
    print("🔧 Enhanced Job Search System Setup:")
    print("✅ Loading configuration from .env file...")
    print("📦 Required packages: pip install crewai langchain langchain-openai requests python-dotenv PyPDF2 pdfplumber")
    print("\n" + "="*50)
    
    try:
        # Resume file path - using 'resume.pdf' as default
        resume_path = "resume.pdf"  # Default resume filename
        
        # Check if resume file exists
        if os.path.exists(resume_path):
            print(f"📄 Found resume file: {resume_path}")
            job_search_system = EnhancedJobSearchAgentSystem(resume_path=resume_path)
        else:
            print(f"⚠️  Resume file not found at: {resume_path}")
            print("💡 Proceeding without resume analysis (general recommendations)")
            print("💡 To use resume analysis, place your resume.pdf in the project directory")
            job_search_system = EnhancedJobSearchAgentSystem()
        
        # Example usage - CUSTOMIZE THESE PARAMETERS
        role = "Senior Data Scientist"
        location = "New York"
        num_results = 5
        
        # Execute personalized job search
        result = job_search_system.search_jobs(
            role=role,
            location=location,
            num_results=num_results
        )
        
        if result:
            print("\n📊 Final Summary:")
            print(result)
        
    except ValueError as e:
        print(f"❌ .env Configuration Error: {e}")
        print("💡 Make sure your .env file exists and contains all required API keys")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
