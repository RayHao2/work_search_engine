from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

print(common_texts)
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
# print(documents)
model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)