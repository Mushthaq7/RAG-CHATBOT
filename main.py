from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
from vector_store import ProductVectorStore
import sqlite3

app = FastAPI(title="ZUS RAG API",
              description="RAG endpoints for ZUS products and outlets.")

# --- Ollama LLM Helper ---


def ollama_chat(prompt, model="llama3"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"].strip()

# --- Product Endpoint ---


class ProductResult(BaseModel):
    name: str
    desc: str


class ProductResponse(BaseModel):
    results: List[ProductResult]
    summary: str


try:
    product_store = ProductVectorStore()
except Exception as e:
    product_store = None
    print(f"Error loading product vector store: {e}")


@app.get("/products", response_model=ProductResponse)
def get_products(query: str = Query(..., description="User question about drinkware products."), top_k: int = 3):
    if not product_store:
        raise HTTPException(
            status_code=500, detail="Product vector store not loaded.")
    try:
        results = product_store.query(query, top_k=top_k)
        context = "\n".join([f"{r['name']}: {r['desc']}" for r in results])
        prompt = f"Given the following ZUS drinkware products, answer the user's question.\n\nProducts:\n{context}\n\nQuestion: {query}\n\nSummary:"
        summary = ollama_chat(prompt)
        return ProductResponse(results=results, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# --- Outlets Endpoint ---


class OutletResult(BaseModel):
    name: str
    address: str
    hours: Optional[str] = None
    services: Optional[str] = None


class OutletResponse(BaseModel):
    sql: str
    results: List[OutletResult]


DB_PATH = 'outlets.db'


@app.get("/outlets", response_model=OutletResponse)
def get_outlets(query: str = Query(..., description="Natural language query about outlets.")):
    schema = "Table: outlets (id, name, address, hours, services)"
    prompt = (
        f"Given the following SQLite table schema:\n"
        f"{schema}\n"
        "Translate the user's question into a SQL SELECT statement. "
        "Only select columns that answer the question. Do not use LIMIT unless asked. "
        "Do not use DELETE/UPDATE/INSERT.\n\n"
        f"User question: {query}\nSQL:"
    )
    try:
        sql = ollama_chat(prompt)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]
        results = [dict(zip(columns, row)) for row in rows]
        outlet_results = [OutletResult(
            **{k: v for k, v in r.items() if k in OutletResult.__fields__}) for r in results]
        conn.close()
        return OutletResponse(sql=sql, results=outlet_results)
    except Exception as e:
        return OutletResponse(sql="", results=[])
