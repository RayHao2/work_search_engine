import json
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello'

#query expansion 
from flask import request

@app.route('/query', methods=['GET'])
def query():
    job_title = request.args.get('job_title')
    education = request.args.get('education')
    country = request.args.get('country')
    city = request.args.get('city')
    salary_range = request.args.get('salary_range')
    experience = request.args.get('experience')

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
        "size": 100
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
    results_list = [hit['_source'] for hit in search_results['hits']['hits']]
    
    return jsonify(results_list)
