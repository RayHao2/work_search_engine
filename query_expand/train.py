import multiprocessing
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from elasticsearch import Elasticsearch
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pickle

def process_doc():
    #Get all the job titles
    # dataset = set()
    # with open("D:\schoolAndWork\large_files\jobs.json", "r") as f:
    #     data = json.load(f)
    #     for d in data:
    #         dataset.add(d["Job Title"])
    # with open("output.txt", "w") as f:
    #     for d in dataset:
    #         print(d, file=f)
    
    #Process all the job title
    stemmer = PorterStemmer()
    dataset = []
    with open("output.txt", "r") as f:
        for line in f:
            processed_job = []
            job = word_tokenize(line)
            print(job)
            for word in job:
                word = stemmer.stem(word).lower()
                processed_job.append(word)
            dataset.append(processed_job)
    print(dataset)   
    with open("dataset.pkl", "wb") as f:
        pickle.dump(dataset,f)

                
                
                
            
    
def train():
    with open("dataset.pkl", "rb") as f:
        dataset = pickle.load(f)
    cores = multiprocessing.cpu_count() 
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(dataset)]
    model = Doc2Vec(documents, vector_size=5, window=5, min_count=1, workers=cores-1)
    model.save("doc2vec.model")


def test():
    with open("dataset.pkl", "rb") as f:
        dataset = pickle.load(f)
    print("Reference Document:")
    print(dataset[0])

    model = Doc2Vec.load("doc2vec.model")

    similar_docs = model.docvecs.most_similar(positive=[model.infer_vector(dataset[0])], topn=3)

    print("\nSimilar Documents:")
    for doc_index, similarity in similar_docs:
        print(f"Document {dataset[doc_index]}, Similarity: {similarity}")


def main():
    # process_doc()
    train()
    test()

if __name__ == "__main__":
    main()
