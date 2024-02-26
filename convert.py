import csv
import json

def detect_encoding(file_path):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1']  # Add more encodings if needed
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Unable to decode the file using available encodings.")

def csv_to_json(csv_file_path, json_file_path):
    encoding = detect_encoding(csv_file_path)
    data = []
    with open(csv_file_path, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


def count_job_in_json(json_file_path):
    with open(json_file_path, "r") as f:
        json_data = json.load(f)
        print(len(json_data)) 
        
    
    
# Example usage:
csv_to_json('job_descriptions.csv', 'jobs.json')
count_job_in_json("jobs.json")
