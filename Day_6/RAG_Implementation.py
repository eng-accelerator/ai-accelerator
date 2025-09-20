# RAG Implementation with LlamaIndex and LanceDB

This notebook demonstrates a complete RAG (Retrieval Augmented Generation) implementation using LlamaIndex and LanceDB. We'll explore three different approaches:

1. **Vector Search Only** - Fast retrieval without LLM generation
2. **HuggingFace API Integration** - Cloud-based LLM with authentication
3. **Local LLM with Ollama** - Complete local solution

## Overview

The notebook covers:
- Data loading and preparation from HuggingFace datasets
- Vector store setup with LanceDB
- Embedding generation with HuggingFace models
- Three different query approaches with increasing complexity
- Utility functions for table exploration and optimization
## 1. Install Required Dependencies
# # Install all required packages
# !pip install llama-index llama-index-vector-stores-lancedb llama-index-embeddings-huggingface llama-index-llms-huggingface-api lancedb datasets -q

# # Additional packages for local LLM and utilities
# !pip install llama-index-llms-ollama requests -q
## 2. Import Libraries and Setup
import os
import lancedb
import subprocess
import requests
import time
from pathlib import Path
from datasets import load_dataset

# LlamaIndex core components
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

# Embedding and vector store
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore

# LLM integrations
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.llms.ollama import Ollama

# Async support for notebooks
import nest_asyncio
nest_asyncio.apply()

print("All libraries imported successfully")
## 3. Data Preparation and Loading
def prepare_data(num_samples=100):
    """
    Load dataset and create document files
    """
    print(f"Loading {num_samples} personas from dataset...")
    
    # Load the personas dataset
    dataset = load_dataset("dvilasuero/finepersonas-v0.1-tiny", split="train")
    
    # Create data directory
    Path("data").mkdir(parents=True, exist_ok=True)
    
    # Save personas as text files and create Document objects
    documents = []
    for i, persona in enumerate(dataset.select(range(min(num_samples, len(dataset))))):
        # Create Document objects for LlamaIndex
        doc = Document(
            text=persona["persona"],
            metadata={
                "persona_id": i,
                "source": "finepersonas-dataset"
            }
        )
        documents.append(doc)
        
        # Optionally save to files as well
        with open(Path("data") / f"persona_{i}.txt", "w", encoding="utf-8") as f:
            f.write(persona["persona"])
    
    print(f"Prepared {len(documents)} documents")
    return documents

# Load the data
documents = prepare_data(num_samples=100)
## 4. LanceDB Vector Store Setup
def setup_lancedb_store(table_name="personas_rag"):
    """
    Initialize LanceDB and create/connect to a table
    """
    print("Setting up LanceDB connection...")
    
    # Create or connect to LanceDB
    db = lancedb.connect("./lancedb_data")
    
    # LlamaIndex will handle table creation with proper schema
    print(f"Connected to LanceDB, table: {table_name}")
    
    return db, table_name

# Setup database connection
db, table_name = setup_lancedb_store()
## 5. Vector Embeddings and Ingestion Pipeline
async def create_and_populate_index(documents, db, table_name):
    """
    Create ingestion pipeline and populate LanceDB with embeddings
    """
    print("Creating embedding model and ingestion pipeline...")
    
    # Initialize embedding model
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
    
    # Create LanceDB vector store
    vector_store = LanceDBVectorStore(
        uri="./lancedb_data",
        table_name=table_name,
        mode="overwrite"  # overwrite existing table
    )
    
    # Create ingestion pipeline
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=20),
            embed_model,
        ],
        vector_store=vector_store,
    )
    
    print("Processing documents and creating embeddings...")
    # Run the pipeline to process documents and store in LanceDB
    nodes = await pipeline.arun(documents=documents)
    print(f"Successfully processed {len(nodes)} text chunks")
    
    return vector_store, embed_model

# Create embeddings and populate vector store
vector_store, embed_model = await create_and_populate_index(documents, db, table_name)
## 6. Option 1: Vector Search Only (No LLM)

This approach provides fast document retrieval without LLM generation. Perfect for finding relevant content quickly.
def perform_vector_search(db, table_name, query_text, embed_model, top_k=5):
    """
    Perform direct vector search on LanceDB
    """
    # Get query embedding
    query_embedding = embed_model.get_text_embedding(query_text)
    
    # Open table and perform search
    table = db.open_table(table_name)
    results = table.search(query_embedding).limit(top_k).to_pandas()
    
    return results

def test_vector_search():
    """
    Test vector search functionality with sample queries
    """
    print("Testing Vector Search (No LLM needed)")
    print("=" * 50)
    
    # Test queries
    queries = [
        "technology and artificial intelligence expert",
        "teacher educator professor",
        "environment climate sustainability", 
        "art culture heritage creative"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        
        # Perform search
        results = perform_vector_search(db, table_name, query, embed_model, top_k=3)
        
        for idx, row in results.iterrows():
            score = row.get('_distance', 'N/A')
            text = row.get('text', 'N/A')
            
            # Format score
            if isinstance(score, (int, float)):
                score_str = f"{score:.3f}"
            else:
                score_str = str(score)
            
            print(f"\nResult {idx + 1} (Score: {score_str}):")
            print(f"{text[:200]}...")

# Run vector search test
test_vector_search()
## 7. Option 2: RAG with HuggingFace API

This approach uses HuggingFace's cloud API for LLM generation. Requires API token authentication.
# Set your HuggingFace API token here
# Get your free token from: https://huggingface.co/settings/tokens
os.environ["HUGGINGFACE_API_KEY"] = "your_token_here"  # Replace with your actual token

def create_query_engine(vector_store, embed_model, llm=None):
    """
    Create a query engine from the vector store
    """
    # Create index from vector store
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )
    
    # Setup LLM if provided
    query_engine_kwargs = {}
    if llm:
        query_engine_kwargs['llm'] = llm
    
    # Create query engine
    query_engine = index.as_query_engine(
        response_mode="tree_summarize",
        **query_engine_kwargs
    )
    
    return query_engine

def query_rag(query_engine, question):
    """
    Query the RAG system and return response
    """
    response = query_engine.query(question)
    return response

async def test_huggingface_rag():
    """
    Test RAG with HuggingFace API
    """
    print("Testing RAG with HuggingFace API")
    print("=" * 40)
    
    try:
        # Initialize HuggingFace LLM with authentication
        llm = HuggingFaceInferenceAPI(
            model_name="HuggingFaceH4/zephyr-7b-beta",
            token=os.environ.get("HUGGINGFACE_API_KEY")
        )
        
        # Create query engine
        query_engine = create_query_engine(vector_store, embed_model, llm)
        
        # Test queries
        queries = [
            "Find personas interested in technology and AI",
            "Who are the educators or teachers in the dataset?",
            "Describe personas working with environmental topics"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            print("-" * 30)
            
            try:
                response = query_rag(query_engine, query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Setup error: {e}")
        print("Make sure to set your HuggingFace API token above")

# Uncomment the line below after setting your API token
# await test_huggingface_rag()
## 8. Option 3: RAG with Local LLM (Ollama)

This approach uses a completely local LLM setup. No internet required after initial setup.
def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"Ollama is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("Ollama is not installed or not in PATH")
    return False

def download_ollama():
    """Download Ollama installer for Windows"""
    print("Downloading Ollama for Windows...")
    
    url = "https://ollama.com/download/OllamaSetup.exe"
    response = requests.get(url)
    
    installer_path = Path("OllamaSetup.exe")
    with open(installer_path, "wb") as f:
        f.write(response.content)
    
    print("Ollama downloaded successfully!")
    print("Please run the installer manually and then continue.")
    print(f"Installer location: {installer_path.absolute()}")
    
    return installer_path

def start_ollama_service():
    """Start Ollama service"""
    try:
        print("Starting Ollama service...")
        subprocess.Popen(["ollama", "serve"], shell=True)
        time.sleep(3)
        print("Ollama service started!")
        return True
    except Exception as e:
        print(f"Failed to start Ollama: {e}")
        return False

def pull_ollama_model(model_name="llama3.2:1b"):
    """Pull a lightweight model for local inference"""
    try:
        print(f"Pulling model: {model_name}")
        result = subprocess.run(["ollama", "pull", model_name], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"Model {model_name} pulled successfully!")
            return True
        else:
            print(f"Failed to pull model: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error pulling model: {e}")
        return False

def setup_ollama():
    """Complete Ollama setup"""
    if not check_ollama_installed():
        print("Ollama needs to be installed.")
        download_ollama()
        return False
    
    if not start_ollama_service():
        return False
    
    if not pull_ollama_model("llama3.2:1b"):
        return False
    
    print("Ollama setup complete!")
    return True

# Check Ollama installation
check_ollama_installed()
async def test_local_llm_rag():
    """
    Test RAG with local Ollama LLM
    """
    print("Testing RAG with Local LLM (Ollama)")
    print("=" * 40)
    
    try:
        # Initialize local Ollama LLM
        llm = Ollama(
            model="llama3.2:1b",
            base_url="http://localhost:11434",
            request_timeout=60.0
        )
        
        # Create query engine
        query_engine = create_query_engine(vector_store, embed_model, llm)
        
        # Test queries
        queries = [
            "Find personas interested in technology and AI",
            "Who are the educators or teachers in the dataset?",
            "Describe personas working with environmental topics"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            print("-" * 30)
            
            try:
                response = query_rag(query_engine, query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error: {e}")
                print("Make sure Ollama is running with: ollama serve")
                
    except Exception as e:
        print(f"Setup error: {e}")
        print("Make sure Ollama is installed and running")

# Uncomment after Ollama setup is complete
# await test_local_llm_rag()
## 9. Utility Functions and Advanced Features
def explore_lancedb_table(db, table_name):
    """
    Explore the structure and content of the LanceDB table
    """
    try:
        table = db.open_table(table_name)
        
        print("Table Schema:")
        print(table.schema)
        
        print(f"\nTotal records: {table.count_rows()}")
        
        print("\nSample records:")
        df = table.to_pandas().head()
        print(df)
        
        return table
    except Exception as e:
        print(f"Error exploring table: {e}")
        return None

def create_filtered_query_engine(db, table_name, embed_model, filter_dict=None):
    """
    Create a query engine with metadata filtering capabilities
    """
    from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator
    
    # Reconnect to existing table
    vector_store = LanceDBVectorStore(
        uri="./lancedb_data",
        table_name=table_name,
        mode="read"
    )
    
    # Create index
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )
    
    # Create query engine with filters if provided
    if filter_dict:
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key=key,
                    value=value,
                    operator=FilterOperator.EQ
                ) for key, value in filter_dict.items()
            ]
        )
        query_engine = index.as_query_engine(
            filters=filters,
            response_mode="tree_summarize"
        )
    else:
        query_engine = index.as_query_engine(
            response_mode="tree_summarize"
        )
    
    return query_engine

async def batch_process_documents(documents, batch_size=50):
    """
    Process documents in batches for large datasets
    """
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        table_name = f"personas_batch_{i//batch_size}"
        
        vector_store = LanceDBVectorStore(
            uri="./lancedb_data",
            table_name=table_name,
            mode="overwrite"
        )
        
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=20),
                embed_model,
            ],
            vector_store=vector_store,
        )
        
        nodes = await pipeline.arun(documents=batch)
        print(f"Processed batch {i//batch_size + 1}: {len(nodes)} nodes")

def show_usage_examples():
    """
    Display usage examples for different scenarios
    """
    print("Usage Examples:")
    print("=" * 30)
    
    print("\n1. Vector Search Only:")
    print("   test_vector_search()")
    
    print("\n2. HuggingFace API RAG:")
    print("   # Set API token first")
    print("   os.environ['HUGGINGFACE_API_KEY'] = 'your_token'")
    print("   await test_huggingface_rag()")
    
    print("\n3. Local LLM RAG:")
    print("   # Install and setup Ollama first")
    print("   setup_ollama()")
    print("   await test_local_llm_rag()")
    
    print("\n4. Explore Database:")
    print("   explore_lancedb_table(db, table_name)")

# Show usage examples
show_usage_examples()
## Summary

This notebook provides three complete RAG implementation approaches:

### Option 1: Vector Search Only
- **Best for**: Fast document retrieval, no generation needed
- **Advantages**: Very fast, no API costs, no setup complexity
- **Use case**: Finding relevant documents, initial exploration

### Option 2: HuggingFace API
- **Best for**: High-quality responses with cloud LLMs
- **Advantages**: Latest models, no local resources needed
- **Requirements**: HuggingFace API token
- **Use case**: Production applications with budget for API calls

### Option 3: Local LLM (Ollama)
- **Best for**: Complete privacy, no internet dependency
- **Advantages**: No API costs, full control, offline capability
- **Requirements**: Ollama installation, local compute resources
- **Use case**: Private data, cost-sensitive applications

Choose the approach that best fits your needs!
