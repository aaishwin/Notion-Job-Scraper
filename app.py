from flask import Flask,jsonify,request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import notion
from scraper import scrape_indeed,get_keywords
load_dotenv()
app=Flask(__name__)
CORS(app)
@app.route('/test',methods=['GET'])
def test_route():
    return jsonify({"message": "SERVER IS UP AND RUNNING"}),200

@app.route('/jobs',methods=['GET'])
def get_jobs_route():
    database_id=os.getenv("NOTION_DATABASE_ID")
    jobs=notion.get_jobs(database_id)
    if jobs:
        return jsonify({"jobs":jobs}),200
    return jsonify({"error":"FAILED TO RETREIVE JOBS"}),500
@app.route('/scrape',methods=['GET'])
def scrape():
    keyword=request.args.get('keyword')
    if not keyword:
        return jsonify({"error":"Keyword parameter is missing"}),400
    app.logger.info(f"scraping for keyword: {keyword}")
    jobs=scrape_indeed(keyword)
    return jsonify({"jobs":jobs}),200
@app.route('/scrape-all', methods=['GET'])
def scrape_all():
    keywords = get_keywords(os.getenv("KEYWORDS_FILE", "keywords.txt"))
    all_jobs = []

    for keyword in keywords:
        app.logger.info(f"Scraping for keyword: {keyword}")
        jobs = scrape_indeed(keyword)
        all_jobs.extend(jobs)

    return jsonify({"jobs": all_jobs}), 200






if __name__=='__main__':
    port=int(os.getenv('PORT',5003))
    app.run(debug=True,port=port)
