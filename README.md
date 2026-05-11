# 📚 RAG-Based Document QA System

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent question-answering over your PDF documents using LangChain, FAISS, and Ollama.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🤖 **Intelligent Q&A**: Ask questions about your documents in natural language
- 🔍 **Semantic Search**: Uses FAISS vector store for efficient similarity search
- 💬 **Modern Chat UI**: Beautiful, responsive interface with chat history
- 🚀 **Local LLM**: Runs completely offline using Ollama (Mistral model)
- 📄 **PDF Support**: Automatically processes and indexes PDF documents
- ⚡ **Fast Retrieval**: Optimized embedding and retrieval pipeline
- 🎨 **Sleek Design**: Gradient UI with smooth animations and loading states

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│  Interface  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Flask     │
│   Backend   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│     LangChain RAG Chain     │
├─────────────┬───────────────┤
│  Retriever  │  LLM (Ollama) │
│   (FAISS)   │   (Mistral)   │
└─────────────┴───────────────┘
       │
       ▼
┌─────────────┐
│   Vector    │
│    Store    │
└─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai) installed
- Conda or virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RAG-based_Document_QA_System.git
   cd RAG-based_Document_QA_System
   ```

2. **Create a virtual environment**
   ```bash
   conda create -n rag-mlops python=3.8
   conda activate rag-mlops
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and set up Ollama**
   ```bash
   # Download from https://ollama.ai
   ollama pull mistral
   ```

5. **Prepare your documents**
   - Place your PDF files in the `data/documents/` directory

6. **Index your documents**
   ```bash
   python -m app.rag.ingest
   ```

7. **Run the application**
   ```bash
   python -m app.flask_app.app
   ```

8. **Open your browser**
   - Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
RAG-based_Document_QA_System/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration settings
│   ├── flask_app/
│   │   ├── __init__.py
│   │   ├── app.py                 # Flask application
│   │   └── templates/
│   │       └── index.html         # Frontend UI
│   └── rag/
│       ├── __init__.py
│       ├── ingest.py              # Document ingestion pipeline
│       ├── retriever.py           # Vector store retriever
│       └── qa_chain.py            # QA chain logic
├── data/
│   └── documents/                 # Place PDF files here
├── vector_store/                  # FAISS vector database
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Edit `app/core/config.py` to customize:

```python
# Data paths
DATA_PATH = BASE_DIR / "data/documents"
VECTOR_DB_PATH = BASE_DIR / "vector_store"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# LLM model
LLM_MODEL = "mistral"
```

## 💡 Usage

1. **Add Documents**: Place PDF files in `data/documents/`
2. **Index**: Run `python -m app.rag.ingest` to create the vector store
3. **Query**: Use the web interface to ask questions
4. **Example Questions**:
   - "What are the main topics in the documents?"
   - "Summarize the key findings"
   - "Explain [specific concept] from the documents"

## 🛠️ Technologies Used

- **LangChain**: LLM orchestration framework
- **FAISS**: Vector similarity search
- **Ollama**: Local LLM runtime
- **Flask**: Web framework
- **HuggingFace**: Sentence transformers for embeddings
- **PyPDF**: PDF document processing

## 📊 MLOps Features

This project demonstrates key MLOps concepts:

- ✅ **Modular Architecture**: Separated concerns (ingestion, retrieval, inference)
- ✅ **Configuration Management**: Centralized config file
- ✅ **Reproducibility**: Requirements file and environment setup
- ✅ **Scalability**: Vector store for efficient retrieval
- ✅ **Local Deployment**: Self-hosted LLM for privacy

## 🔮 Future Enhancements

- [ ] Add Docker containerization
- [ ] Implement MLflow for experiment tracking
- [ ] Add Prometheus/Grafana for monitoring
- [ ] Support multiple document formats (Word, TXT, HTML)
- [ ] Add user authentication
- [ ] Implement conversation memory
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add CI/CD pipeline
- [ ] Implement A/B testing for different models
- [ ] Add unit and integration tests

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'app'`
- **Solution**: Run from project root: `python -m app.flask_app.app`

**Issue**: `Ollama call failed with status code 404`
- **Solution**: Pull the model: `ollama pull mistral`

**Issue**: Empty responses
- **Solution**: Check if documents are indexed and Ollama is running

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- LangChain team for the amazing framework
- Ollama for local LLM capabilities
- HuggingFace for sentence transformers

---

⭐ **Star this repo if you found it helpful!**
