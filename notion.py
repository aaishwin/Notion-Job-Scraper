from notion_client import Client
import os
from dotenv import load_dotenv
load_dotenv()
jobs=set()
notion = Client(auth=os.getenv("NOTION_API_KEY"))

def get_jobs(database_id):
    try:
        response=notion.databases.query(database_id=database_id)
        for result in response.get("results",[]):
            job_id=result["id"]
            jobs.add(job_id)
        return list(jobs)
    except Exception as e:
        print(f" Error, not getting jobs from notion {e}")
        return None
    
def add_jobs(database_id,job_data,):
    try:
        response=notion.pages.create(parent={"database_id":database_id},properties=job_data)
        job_id=response.get("id")
        jobs.add(job_id)
    except Exception as e:
        print(f"Error adding job to Notion: {e}")
        return None

def job_exists(job_id):
    return job_id in jobs





