import json
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flask import request
import math
app = Flask(__name__)


#To run: flask --app query_api run
@app.route('/')

def index():
    return 'Hello'



def job_titile_expand():
    pass
@app.route('/query', methods=['GET'])
def query():
    #job search parameters 
    job_title = request.args.get('job_title')
    education = request.args.get('education')
    country = request.args.get('country')
    city = request.args.get('city')
    salary_range = request.args.get('salary_range')
    experience = request.args.get('experience')
    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default page is 1
    page_size = int(request.args.get('page_size', 10))  # Default page size is 10

    es = Elasticsearch('https://localhost:9200', basic_auth=("elastic", "B_mJvwy5xsSJdNwjcAx9"), verify_certs=False)
    index_name = "jobs_index"
    
    search_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"Job Title": job_title}},
                ]
            }
        },
        "from": (page - 1) * page_size,  # Calculate the starting index for pagination
        "size": page_size  # Set the number of results per page
    }

    if education is not None:
        search_query["query"]["bool"]["must"].append({"match": {"Qualifications": education}})
    if country is not None:
        search_query["query"]["bool"]["must"].append({"match": {"Country": country}})
    if city is not None:
        search_query["query"]["bool"]["must"].append({"match": {"location": city}})
    if salary_range is not None:
        search_query["query"]["bool"]["must"].append({"match": {"Salary Range": salary_range}})
    if experience is not None:
        search_query["query"]["bool"]["must"].append({"match": {"Experience": experience}})
        
    search_results = es.search(index=index_name, body=search_query)
    total_hits = search_results['hits']['total']['value']
    results_list = [hit['_source'] for hit in search_results['hits']['hits']]
    
    # Calculate total pages
    total_pages = math.ceil(total_hits / page_size)

    # Return the results along with pagination metadata
    response = {
        "total_pages": total_pages,
        "current_page": page,
        "results": results_list,
    }

    return jsonify(response)

