import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import random
import time
import requests
load_dotenv()
KEYWORDS_FILE=os.getenv("KEYWORDS_FILE","keywords.txt")
def get_keywords(file_path):
    try:
        with open(file_path,'r') as file:
            keywords=[line.strip() for line in file.readlines()]
        return keywords
    except Exception as e:
        print("ERROR READING KEYWORDS FILE")
        return []
    
USER_AGENTS=[ "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko ) Chrome/91.0.4472.114 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 Like Mac OS X ) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1,","Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"]


def scrape_indeed(keyword):
    """
    Scrapes job listings from Indeed based on a given keyword.
    Args:
        keyword (str): The job search keyword to query (e.g., "Software Developer").
    Returns:
        list: A list of dictionaries containing job details (title, company, location).
              If an error occurs, a list with an error message is returned.
    """
    url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l="        # Construct search URL with query
    headers = {                                                                   # Set user-agent to avoid blocking
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"}
    try:
        response = requests.get(url, headers=headers)                            # Send GET request to Indeed
        response.raise_for_status()                                             # Raise error for HTTP issues
        soup = BeautifulSoup(response.content, "lxml")                         # Parse HTML content
        job_listings = []

        for job_card in soup.select(".result"):                                # Iterate through job cards
            title = job_card.select_one(".jobTitle").text.strip() if job_card.select_one(".jobTitle") else "N/A"
            company = job_card.select_one(".companyName").text.strip() if job_card.select_one(".companyName") else "N/A"
            location = job_card.select_one(".companyLocation").text.strip() if job_card.select_one(".companyLocation") else "N/A"

            job_listings.append({                                               # Append job data to the list
                "title": title,
                "company": company,
                "location": location,
            })

        return job_listings                                                     # Return the list of job listings

    except requests.RequestException as e:                                      # Handle network-related errors
        print(f"Network error while scraping {keyword}: {e}")
        return [{"error": f"Network error for '{keyword}': {str(e)}"}]

    except Exception as e:                                                      # Handle unexpected errors
        print(f"Unexpected error while scraping {keyword}: {e}")
        return [{"error": f"Error scraping '{keyword}': {str(e)}"}]



    
def main():
    keywords=get_keywords(KEYWORDS_FILE)
    all_jobs=[]
    for keyword in keywords:
        print(f"scraping for job: {keyword}")
        jobs=scrape_indeed(keyword)
        all_jobs.extend(jobs)
    print(f"found {len(all_jobs)} job listings for you to apply to!")
    for job in all_jobs:
        print(job)
    
if __name__=="__main__":
    main()





