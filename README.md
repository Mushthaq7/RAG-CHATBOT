# RAG Chatbot for Product Recommendations

A Retrieval-Augmented Generation (RAG) chatbot system that provides intelligent product recommendations based on user queries. This system uses vector embeddings and semantic search to find relevant products and generate contextual responses.

## Features

- **Semantic Product Search**: Uses vector embeddings to find products based on meaning, not just exact text matches
- **Intelligent Recommendations**: Provides contextual product recommendations with detailed descriptions
- **Interactive Chat Interface**: Simple command-line interface for testing the chatbot
- **Product Database**: Stores product information with descriptions and metadata
- **Vector Store**: Efficient storage and retrieval of product embeddings

## Project Structure

- `main.py` - Main application entry point
- `product_ingest.py` - Product data ingestion and processing
- `outlet_ingest.py` - Outlet/store data ingestion
- `vector_store.py` - Vector store management and operations
- `chatbot_demo.py` - Interactive chatbot demonstration
- `requirements.txt` - Python dependencies

## Setup

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**:
   Create a `.env` file with your API keys:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

### Interactive Chatbot Demo

```bash
python chatbot_demo.py
```

This will start an interactive session where you can ask questions about products and receive intelligent recommendations.

### Product Ingestion

```bash
python product_ingest.py
```

This processes product data and creates vector embeddings for semantic search.

### Outlet Ingestion

```bash
python outlet_ingest.py
```

This processes outlet/store data for location-based recommendations.

## How It Works

1. **Data Ingestion**: Product and outlet data is processed and stored in a structured format
2. **Vector Embeddings**: Product descriptions are converted to vector embeddings using OpenAI's embedding model
3. **Semantic Search**: User queries are converted to embeddings and matched against product embeddings
4. **RAG Response**: The system retrieves relevant products and generates contextual responses using GPT

## Technologies Used

- **OpenAI API**: For embeddings and text generation
- **SQLite**: Local database storage
- **FAISS**: Vector similarity search
- **Python**: Core application logic

## Example Queries

- "I need a coffee mug for hot drinks"
- "Show me cold drink containers"
- "I want something for iced coffee"
- "Looking for travel-friendly drinkware"

The system will provide relevant product recommendations with detailed descriptions and usage suggestions.
