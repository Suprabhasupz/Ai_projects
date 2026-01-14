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
