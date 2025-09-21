# Day 6 Session 2 - RAG Assignments

This directory contains assignments for Day 6 Session 2, focusing on building RAG (Retrieval-Augmented Generation) systems with LlamaIndex.

## Assignment 1: Vector Database Creation and Retrieval

**File:** `assignment_1_vector_db_basics.ipynb`  
**Solution:** `assignment_1_solution.ipynb`

### Objective
Learn the fundamentals of vector databases by creating a complete document indexing and retrieval system.

### Learning Goals
- Understand document loading with `SimpleDirectoryReader`
- Learn vector store setup with LanceDB
- Implement vector index creation with `StorageContext`
- Perform semantic search and retrieval
- Use local embeddings (no OpenAI API key required)
- Configured for OpenRouter compatibility (when LLM needed)

### What You'll Build
1. **Document Loader**: Load documents from a folder using `SimpleDirectoryReader`
2. **Vector Store**: Create a LanceDB vector store for embeddings
3. **Index Creator**: Build a vector index from documents
4. **Search Function**: Implement semantic search functionality

### Instructions
1. Open `assignment_1_vector_db_basics.ipynb`
2. Complete each function by replacing the TODO comments
3. Run each cell after completing the function to test it
4. Refer to the existing notebooks in `llamaindex_rag/` folder for examples
5. Use `assignment_1_solution.ipynb` to check your answers

### API Configuration
- ✅ **No OpenAI API key required** - uses local embeddings
- ✅ **OpenRouter ready** - configured for future LLM operations
- ✅ **Cost-effective** - all vector operations run locally

### Key Concepts Covered
- **SimpleDirectoryReader**: Loading documents from folders
- **LanceDBVectorStore**: Vector storage with LanceDB
- **StorageContext**: Managing storage components
- **VectorStoreIndex**: Creating searchable indexes
- **Semantic Retrieval**: Finding relevant documents by meaning

### Expected Output
After completing all functions, you should be able to:
- Load documents from the `../data` folder
- Create a vector database
- Search for documents using natural language queries
- Get relevant results with similarity scores

### Tips
- The data folder contains diverse file types (PDFs, CSVs, Markdown, HTML, etc.)
- SimpleDirectoryReader handles multiple file formats automatically
- Use `recursive=True` to load files from subdirectories
- LanceDB provides efficient vector storage and retrieval
- The similarity scores help evaluate result relevance

## Dataset
The assignment uses the data in `../data/` which includes:
- AI research papers (PDFs)
- Agent evaluation metrics (CSV)
- Cooking recipes (Markdown, CSV)
- Financial data (CSV, Markdown)
- Health tracking data (HTML)
- Travel guides (Markdown)
- Various images

This diverse dataset demonstrates the multimodal capabilities of the RAG system.

## Getting Help
If you get stuck:
1. Check the existing notebooks in `llamaindex_rag/` for examples
2. Look at the solution file for guidance
3. Review the LlamaIndex documentation
4. Ask for help during the session

## Assignment 2: Advanced RAG Techniques

**File:** `assignment_2_advanced_rag.ipynb`  
**Solution:** `assignment_2_solution.ipynb`

### Objective
Master advanced RAG techniques that transform basic document retrieval into production-ready, intelligent systems.

### Learning Goals
- Understand and implement node postprocessors for filtering and reranking
- Learn different response synthesis strategies (TreeSummarize, Refine)
- Create structured outputs using Pydantic models  
- Build advanced retrieval pipelines with multiple processing stages

### Prerequisites
- Complete Assignment 1 first
- Understanding of basic vector databases and retrieval

### What You'll Build
1. **Similarity Postprocessor**: Filter low-relevance results for better precision
2. **TreeSummarize Engine**: Create comprehensive analytical responses
3. **Structured Output System**: Generate type-safe JSON responses
4. **Advanced Pipeline**: Combine all techniques into production-ready system

### Advanced Concepts Covered
- **Node Postprocessors**: `SimilarityPostprocessor` for result filtering
- **Response Synthesizers**: `TreeSummarize` for complex analysis
- **Structured Outputs**: `PydanticOutputParser` for type-safe responses
- **Advanced Pipelines**: Combining multiple techniques

### Instructions
1. Complete Assignment 1 before starting this one
2. Open `assignment_2_advanced_rag.ipynb`
3. Complete each function by replacing the TODO comments
4. Run each cell after completing the function to test it
5. Refer to the `03_advanced_rag_techniques.ipynb` notebook for examples
6. Use `assignment_2_solution.ipynb` to check your answers

### API Configuration
- ✅ **OpenRouter LLM required** - for response synthesis
- ✅ **Local embeddings** - cost-effective vector operations
- ⚠️ **LLM operations** - needed for advanced response synthesis

### Expected Output
After completing all functions, you should be able to:
- Filter search results based on relevance scores
- Generate comprehensive analytical responses
- Receive structured JSON outputs instead of free text
- Compare basic vs advanced RAG performance

### Key Benefits
- **Better Precision**: Similarity filtering removes irrelevant results
- **Comprehensive Analysis**: TreeSummarize provides deeper insights
- **Reliable Integration**: Structured outputs enable system integration
- **Production Ready**: Advanced pipelines suitable for real applications

## Assignment 3a: Basic Gradio RAG Frontend

**File:** `assignment_3a_basic_gradio_rag.ipynb`

### Objective
Build a simple Gradio frontend for your RAG system with essential features only - perfect for learning Gradio fundamentals.

### Learning Goals
- Create basic Gradio interfaces
- Connect RAG backend to frontend
- Handle user interactions and database initialization
- Build functional AI-powered web applications

### Prerequisites
- Complete Assignments 1 & 2
- Basic understanding of Gradio from Day 2

### What You'll Build
**Essential Features Only:**
1. **Initialize Database Button**: Set up vector database with one click
2. **Search Query Input**: Text input for user questions
3. **Submit Button**: Process queries and get responses
4. **Response Display**: Show AI-generated answers
5. **Status Messages**: Display initialization and error messages

### Key Components
- `gr.Blocks()` for custom layout
- `gr.Button()` for initialization and search
- `gr.Textbox()` for input and output
- Simple event handling with `.click()`

### Instructions
1. Complete Assignments 1 & 2 first
2. Open `assignment_3a_basic_gradio_rag.ipynb`
3. Follow the step-by-step implementation
4. Test your interface after each section

### Expected Output
A simple but functional RAG web interface where users can:
- Initialize the vector database
- Ask questions and receive AI responses
- Get clear status messages

<img width="1882" height="979" alt="Screenshot 2025-09-21 at 9 11 55 AM" src="https://github.com/user-attachments/assets/0ecc56d4-8dc1-435a-b2e5-ef2f003bcbaa" />

---

## Assignment 3b: Advanced Gradio RAG Frontend

**File:** `assignment_3b_advanced_gradio_rag.ipynb`

### Objective
Extend your basic RAG interface with advanced configuration options to create a professional, feature-rich application.

### Learning Goals
- Advanced Gradio components and interactions
- Dynamic RAG configuration
- Professional UI design patterns
- Parameter validation and handling
- Building production-ready AI applications

### Prerequisites
- Complete Assignment 3a (Basic Gradio RAG)
- Understanding of RAG parameters and their effects

### What You'll Build
**Advanced Configuration Features:**
1. **Model Selection**: Dropdown for gpt-4o, gpt-4o-mini, gpt-4o-nano
2. **Temperature Control**: Slider (0 to 1, step 0.1)
3. **Chunk Configuration**: Size and overlap inputs
4. **Similarity Top-K**: Slider for number of documents to retrieve
5. **Node Postprocessors**: Multiselect for filtering options
6. **Similarity Cutoff**: Slider for relevance filtering
7. **Response Synthesizers**: Dropdown for TreeSummarize, Refine, etc.
8. **Configuration Display**: Show current parameter settings

### Advanced UI Components
- **Model Dropdown**: `gr.Dropdown()` with predefined options
- **Parameter Sliders**: `gr.Slider()` with custom ranges and steps
- **Multi-select**: `gr.CheckboxGroup()` for postprocessor selection
- **Number Inputs**: `gr.Number()` for chunk size/overlap
- **Professional Layout**: `gr.Row()` and `gr.Column()` for organization

### Instructions
1. Complete Assignment 3a first (basic interface)
2. Open `assignment_3b_advanced_gradio_rag.ipynb`
3. Implement the advanced backend with configurable parameters
4. Build the sophisticated interface with all controls
5. Test different parameter combinations
6. Experiment with various configurations to understand their effects

### API Configuration
- ✅ **Dynamic LLM selection** - Choose between different models
- ✅ **Configurable parameters** - Adjust all RAG settings in real-time
- ✅ **OpenRouter integration** - for multiple model access
- ✅ **Local embeddings** - cost-effective vector operations

### Expected Output
A professional RAG interface with:
- Full parameter control and real-time configuration
- Clear display of current settings
- Professional layout and user experience
- Ability to experiment with different RAG approaches

<img width="1804" height="983" alt="Screenshot 2025-09-21 at 9 39 22 AM" src="https://github.com/user-attachments/assets/37a6cbb4-baed-480e-a355-8c3cba1ad38b" />


### Key Benefits
- **Parameter Understanding**: Learn how different settings affect RAG performance
- **Production Patterns**: Build interfaces suitable for real applications
- **User Control**: Give users fine-grained control over AI behavior
- **Experimentation**: Easy A/B testing of different configurations

### Configuration Learning
Through this assignment, you'll understand:
- **Model Selection**: When to use different GPT models
- **Temperature Effects**: How creativity vs accuracy is controlled
- **Chunking Strategy**: Impact of chunk size and overlap on retrieval
- **Filtering Techniques**: How similarity cutoffs improve precision
- **Synthesis Methods**: Different approaches to combining retrieved information

---

## Assignment Solutions

**Solution Files:**
- `assignment_1_solution.ipynb` - Vector Database Basics
- `assignment_2_solution.ipynb` - Advanced RAG Techniques  
- `assignment_3a_solution.ipynb` - Basic Gradio RAG Frontend
- `assignment_3b_solution.ipynb` - Advanced Gradio RAG Frontend

### Real-World Applications
Both assignments prepare you for building:
- **Knowledge Management**: Internal company document search
- **Research Assistant**: Academic paper analysis and Q&A
- **Customer Support**: Automated help desk with document knowledge
- **Educational Tools**: Interactive learning from course materials
- **Content Discovery**: Smart search through large document collections

### Deployment Options
- **Local**: Run on your machine for development
- **Shared**: Create public links for team access  
- **Cloud**: Deploy to platforms like Hugging Face Spaces
- **Enterprise**: Integrate into existing web applications

Good luck! 🚀
