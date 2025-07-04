import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class ProductVectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index('products.index')
        with open('products.pkl', 'rb') as f:
            self.products = pickle.load(f)

    def query(self, user_query, top_k=3):
        emb = self.model.encode([user_query])
        D, I = self.index.search(np.array(emb).astype('float32'), top_k)
        results = [self.products[i] for i in I[0]]
        return results
