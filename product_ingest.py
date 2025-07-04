import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Scrape ZUS Drinkware products


def scrape_drinkware():
    url = 'https://shop.zuscoffee.com/collections/drinkware'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    products = []
    for item in soup.select('.product-card'):
        name = item.select_one('.product-card__title').get_text(strip=True)
        desc = item.select_one('.product-card__description')
        desc = desc.get_text(strip=True) if desc else ''
        products.append({'name': name, 'desc': desc})
    return products

# Ingest into FAISS vector store


def ingest_to_faiss(products, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    texts = [f"{p['name']}: {p['desc']}" for p in products]
    embeddings = model.encode(texts, show_progress_bar=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    # Save index and metadata
    faiss.write_index(index, 'products.index')
    with open('products.pkl', 'wb') as f:
        pickle.dump(products, f)
    print(f"Ingested {len(products)} products into FAISS.")


if __name__ == '__main__':
    products = scrape_drinkware()
    ingest_to_faiss(products)
