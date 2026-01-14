# 📚 Books Application

A Python application that fetches book data from a REST API and stores it in a SQLite database.

## 📁 Project Structure

```
books_app/
├── api/
│   └── server.py        # Flask API server (100 books)
├── db/
│   ├── database.py      # SQLite database operations
│   └── books.db         # SQLite database (auto-created)
├── services/
│   └── api_client.py    # API client for fetching data
├── run.py               # Main entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

This single command will:
1. Start the Flask API server (background)
2. Create the SQLite database
3. Fetch 100 books from the API
4. Store books in the database
5. Display the results

## 🔗 API Endpoints

When running, the API is available at:

| Endpoint | Description |
|----------|-------------|
| `GET /` | API welcome message |
| `GET /books` | Get all 100 books |
| `GET /books/<id>` | Get a specific book by ID |

## 📖 Example Response

```json
{
    "id": 1,
    "title": "The Silent Echo II",
    "author": "Jane Austen",
    "publication_year": 1995
}
```

## 🛠️ Running Components Separately

### Run only the API server:
```bash
python -m api.server
```

### Run as a module:
```bash
python -c "from db.database import display_books, create_database; display_books(create_database())"
```


# AI & Software Engineering Assignment

This repository contains solutions to a multi-part assignment covering data engineering, visualization, large language model (LLM) architecture, vector databases, and robotics. The focus is on clean design, scalability, and real-world applicability rather than only code execution.

---

## 📌 Problem Statement 1: API Data Retrieval & Storage

### Overview
A high-level, research-oriented approach to fetching book data from a REST API, validating it, storing it in an SQLite database, and displaying the results.

### Workflow
1. Fetch JSON data from a REST API
2. Validate required fields (title, author, year)
3. Create an SQLite database and table
4. Store validated records
5. Retrieve and display stored data

### Key Concepts
- RESTful APIs
- Data validation
- SQLite database design
- Modular Python architecture

---

## 📊 Data Processing & Visualization

This module demonstrates:
- Fetching data from an API using `requests`
- Processing data using `pandas`
- Computing averages
- Visualizing results using `matplotlib`

This showcases a complete data pipeline from ingestion to insight.

---

## 📁 CSV to SQLite Automation

A Python script that:
- Reads user data from a CSV file
- Automatically creates an SQLite database
- Inserts records into structured tables
- Retrieves and prints data for verification

Use case: lightweight data migration and local persistence.

---

## 🤖 LLM Chatbot Architecture (High-Level Design)

The chatbot design includes:

- **UI Layer** – User interaction (web/app)
- **Orchestration Layer** – Controls flow and tool usage
- **LLM** – Core reasoning and response generation
- **RAG (Retrieval-Augmented Generation)**
  - Embeddings
  - Vector database
- **Context & Memory Management**
- **Tool & API Integration**
- **Backend & Deployment** – FastAPI, Docker, cloud infrastructure

This architecture enables scalable, accurate, and context-aware conversational AI systems.




