from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import time


def indexing():
    es = Elasticsearch('https://localhost:9200', basic_auth=("elastic",
                                                             "B_mJvwy5xsSJdNwjcAx9"), verify_certs=False)

    with open("jobs.json", "r") as f:
        data = json.load(f)
        keys = list(data[0].keys())
        # print(keys)
    index_name = "jobs_index"
    # helpers.bulk(es,docs)
    docs = []
    for d in data:
        doc_e = {
            '_index': index_name,
        }
        for key in keys:
            if key == 'Job Id':
                doc_e["_id"] = d[key]
            doc_e[key] = d[key]
        docs.append(doc_e)
    helpers.bulk(es, docs)
    print("===================== Index Done ===================== ")


def query():
    es = Elasticsearch('https://localhost:9200', basic_auth=("elastic",
                                                             "B_mJvwy5xsSJdNwjcAx9"), verify_certs=False)

    # keys
    # ['Job Id', 'Experience', 'Qualifications', 'Salary Range', 'location', 'Country', 'latitude', 'longitude',
    # 'Work Type', 'Company Size', 'Job Posting Date', 'Preference', 'Contact Person', 'Contact',
    # 'Job Title', 'Role', 'Job Portal', 'Job Description', 'Benefits', 'skills', 'Responsibilities', 'Company', 'Company Profile']
    search_query = {
        "query": {
            "match": {
                "Qualifications": "MBA"
            }
        }
    }
    
    index_name = "jobs_index"
    doc_count = es.count(index=index_name)['count']

    # Print the document count
    print(f"The number of documents in index '{index_name}' is: {doc_count}")
    
    
    # search_results = es.search(index=index_name, body=search_query)

    # with open("output.txt", "w") as f:
    #     # Process search results
    #     for hit in search_results['hits']['hits']:
    #         print(hit['_source'], file=f)


def main():
    # indexing()
    query()


if __name__ == "__main__":
    main()
