{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "9af77a6d",
   "metadata": {},
   "source": [
    "# 📚 Books Application\n",
    "\n",
    "This Jupyter notebook demonstrates a complete Books Application that:\n",
    "1. **Starts a Flask API server** - Serves random book data via REST endpoints\n",
    "2. **Creates a SQLite database** - Local storage for book information\n",
    "3. **Fetches books from API** - Uses requests library to get data\n",
    "4. **Stores and displays books** - Persists data and shows formatted output\n",
    "\n",
    "## Features\n",
    "- RESTful API with Flask\n",
    "- SQLite database operations\n",
    "- HTTP client for API consumption\n",
    "- Multi-threaded server execution"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ae56bb9d",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# INSTALL DEPENDENCIES\n",
    "\n",
    "pip3 install flask requests\n",
    "\n",
    "# After installation, restart the kernel before running other cells"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8673189d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ All libraries imported successfully!\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# Flask framework for creating the REST API server\n",
    "from flask import Flask, jsonify\n",
    "\n",
    "# SQLite for local database storage\n",
    "import sqlite3\n",
    "\n",
    "# Requests library for HTTP API calls\n",
    "import requests\n",
    "\n",
    "# Standard library imports\n",
    "import random      # For generating random book data\n",
    "import threading   # For running server in background thread\n",
    "import time        # For adding delays\n",
    "import os          # For file path operations\n",
    "from typing import List, Dict  # Type hints for better code documentation\n",
    "\n",
    "print(\"✓ All libraries imported successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "55a29333",
   "metadata": {},
   "source": [
    "## 2. Flask API Server Setup\n",
    "\n",
    "The Flask API server provides endpoints to serve book data. This section defines:\n",
    "- Sample data (authors and book titles)\n",
    "- Book generation function\n",
    "- REST API endpoints"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "91915f2e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Loaded 20 authors and 50 book titles\n"
     ]
    }
   ],
   "source": [
    "\n",
    "# Create Flask application instance\n",
    "# Flask(__name__) uses the current module name for configuration\n",
    "app = Flask(__name__)\n",
    "\n",
    "# -----------------------------------------------------------------------------\n",
    "# Lists of authors and book titles for generating random books\n",
    "# -----------------------------------------------------------------------------\n",
    "\n",
    "# Famous authors from various genres and time periods\n",
    "AUTHORS = [\n",
    "    \"Jane Austen\", \"Charles Dickens\", \"Mark Twain\", \"Ernest Hemingway\",\n",
    "    \"Virginia Woolf\", \"George Orwell\", \"F. Scott Fitzgerald\", \"Leo Tolstoy\",\n",
    "    \"Gabriel García Márquez\", \"Toni Morrison\", \"Haruki Murakami\", \"J.K. Rowling\",\n",
    "    \"Stephen King\", \"Agatha Christie\", \"Oscar Wilde\", \"Franz Kafka\",\n",
    "    \"Albert Camus\", \"Hermann Hesse\", \"Paulo Coelho\", \"Dan Brown\"\n",
    "]\n",
    "\n",
    "# Creative book titles for random generation\n",
    "TITLES = [\n",
    "    \"The Silent Echo\", \"Midnight Dreams\", \"Beyond the Horizon\", \"Whispers in Time\",\n",
    "    \"The Last Chapter\", \"Shadows of Tomorrow\", \"The Hidden Path\", \"Echoes of War\",\n",
    "    \"The Forgotten Kingdom\", \"Secrets of the Heart\", \"The Crystal Tower\", \"Dancing with Destiny\",\n",
    "    \"The Iron Gate\", \"Waves of Change\", \"The Burning Sky\", \"Lost in Translation\",\n",
    "    \"The Golden Compass\", \"River of Stars\", \"The Midnight Garden\", \"Winds of Fortune\",\n",
    "    \"The Silent Witness\", \"Broken Promises\", \"The Dark Mirror\", \"Songs of Freedom\",\n",
    "    \"The Empty Throne\", \"Chasing Shadows\", \"The Final Hour\", \"Dreams of Glory\",\n",
    "    \"The Wandering Soul\", \"Bridges of Hope\", \"The Sacred Fire\", \"Tales of Wonder\",\n",
    "    \"The Crimson Rose\", \"Voices from Beyond\", \"The Shattered Glass\", \"Journeys End\",\n",
    "    \"The Hollow Crown\", \"Storms of Passion\", \"The Velvet Night\", \"Legends Reborn\",\n",
    "    \"The Amber Stone\", \"Faces in the Crowd\", \"The Frozen Lake\", \"Whispers of Love\",\n",
    "    \"The Rising Sun\", \"Depths of Despair\", \"The Silver Lining\", \"Masks of Deceit\",\n",
    "    \"The Endless Road\", \"Colors of Autumn\"\n",
    "]\n",
    "\n",
    "print(f\"✓ Loaded {len(AUTHORS)} authors and {len(TITLES)} book titles\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8216fddd",
   "metadata": {},
   "source": [
    "### Book Generation Function\n",
    "This function creates random book entries with unique IDs, titles, authors, and publication years."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dc76c902",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Generated 100 random books\n",
      "  Sample: {'id': 1, 'title': 'Waves of Change III', 'author': 'Toni Morrison', 'publication_year': 2022}\n"
     ]
    }
   ],
   "source": [
    "def generate_books(count: int = 100) -> List[Dict]:\n",
    "    \"\"\"\n",
    "    Generate a list of random books.\n",
    "    \n",
    "    This function creates book dictionaries with random combinations of:\n",
    "    - Unique sequential ID\n",
    "    - Title (randomly selected from TITLES, optionally with Roman numeral suffix)\n",
    "    - Author (randomly selected from AUTHORS)\n",
    "    - Publication year (random year between 1850 and 2025)\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    count : int, optional\n",
    "        Number of books to generate (default: 100)\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    List[Dict]\n",
    "        List of book dictionaries with keys: id, title, author, publication_year\n",
    "    \n",
    "    Example:\n",
    "    --------\n",
    "    >>> books = generate_books(5)\n",
    "    >>> print(books[0])\n",
    "    {'id': 1, 'title': 'The Silent Echo II', 'author': 'Jane Austen', 'publication_year': 1920}\n",
    "    \"\"\"\n",
    "    books = []\n",
    "    \n",
    "    for i in range(count):\n",
    "        # Create a book dictionary with random data\n",
    "        book = {\n",
    "            \"id\": i + 1,  # Unique sequential ID starting from 1\n",
    "            # Combine random title with optional Roman numeral (I, II, III, or empty)\n",
    "            \"title\": f\"{random.choice(TITLES)} {random.choice(['I', 'II', 'III', ''])}\".strip(),\n",
    "            \"author\": random.choice(AUTHORS),  # Random author from list\n",
    "            \"publication_year\": random.randint(1850, 2025)  # Random year in range\n",
    "        }\n",
    "        books.append(book)\n",
    "    \n",
    "    return books\n",
    "\n",
    "# Generate 100 books at startup for the API to serve\n",
    "BOOKS = generate_books(100)\n",
    "print(f\"✓ Generated {len(BOOKS)} random books\")\n",
    "print(f\"  Sample: {BOOKS[0]}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4cc3be82",
   "metadata": {},
   "source": [
    "### Flask API Routes\n",
    "Define the REST API endpoints for serving book data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5fe2bc2c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Flask routes defined: /, /books, /books/<id>\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# FLASK API ROUTES\n",
    "# =============================================================================\n",
    "\n",
    "@app.route('/')\n",
    "def home():\n",
    "    \"\"\"\n",
    "    Home endpoint - Returns API welcome message and available endpoints.\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    JSON response with welcome message and endpoint documentation\n",
    "    \"\"\"\n",
    "    return jsonify({\n",
    "        \"message\": \"Welcome to the Books API\",\n",
    "        \"endpoints\": {\n",
    "            \"/books\": \"Get all books\",\n",
    "            \"/books/<id>\": \"Get a specific book by ID\"\n",
    "        }\n",
    "    })\n",
    "\n",
    "@app.route('/books')\n",
    "def get_all_books():\n",
    "    \"\"\"\n",
    "    Get all books endpoint - Returns complete list of books.\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    JSON array containing all 100 generated books\n",
    "    \"\"\"\n",
    "    return jsonify(BOOKS)\n",
    "\n",
    "@app.route('/books/<int:book_id>')\n",
    "def get_book(book_id: int):\n",
    "    \"\"\"\n",
    "    Get single book endpoint - Returns a specific book by its ID.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    book_id : int\n",
    "        The unique identifier of the book to retrieve\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    JSON object with book data, or 404 error if not found\n",
    "    \"\"\"\n",
    "    # Search for book with matching ID using generator expression\n",
    "    book = next((b for b in BOOKS if b[\"id\"] == book_id), None)\n",
    "    \n",
    "    if book:\n",
    "        return jsonify(book)\n",
    "    \n",
    "    # Return 404 error if book not found\n",
    "    return jsonify({\"error\": \"Book not found\"}), 404\n",
    "\n",
    "print(\"✓ Flask routes defined: /, /books, /books/<id>\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "399830e2",
   "metadata": {},
   "source": [
    "### Server Functions\n",
    "Functions to run the Flask server, including background thread execution."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8b127f86",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Server functions defined\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# SERVER FUNCTIONS\n",
    "# =============================================================================\n",
    "\n",
    "def run_server(host: str = '127.0.0.1', port: int = 5000):\n",
    "    \"\"\"\n",
    "    Run the Flask server (blocking).\n",
    "    \n",
    "    This function starts the Flask development server and blocks\n",
    "    until the server is stopped. Use start_server_thread() for\n",
    "    non-blocking execution.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    host : str, optional\n",
    "        The hostname to bind to (default: '127.0.0.1' for localhost)\n",
    "    port : int, optional\n",
    "        The port number to listen on (default: 5000)\n",
    "    \"\"\"\n",
    "    # debug=False prevents auto-reload in production\n",
    "    # use_reloader=False prevents double startup in threaded mode\n",
    "    app.run(host=host, port=port, debug=False, use_reloader=False)\n",
    "\n",
    "\n",
    "def start_server_thread(host: str = '127.0.0.1', port: int = 5000):\n",
    "    \"\"\"\n",
    "    Start the Flask server in a background thread.\n",
    "    \n",
    "    This allows the server to run concurrently while other code\n",
    "    executes. The thread is set as daemon=True so it automatically\n",
    "    stops when the main program exits.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    host : str, optional\n",
    "        The hostname to bind to (default: '127.0.0.1')\n",
    "    port : int, optional\n",
    "        The port number to listen on (default: 5000)\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    threading.Thread\n",
    "        The thread object running the server\n",
    "    \"\"\"\n",
    "    # Create a daemon thread for the server\n",
    "    # daemon=True means thread will stop when main program exits\n",
    "    server_thread = threading.Thread(\n",
    "        target=run_server, \n",
    "        args=(host, port), \n",
    "        daemon=True\n",
    "    )\n",
    "    server_thread.start()\n",
    "    return server_thread\n",
    "\n",
    "print(\"✓ Server functions defined\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8e2427e9",
   "metadata": {},
   "source": [
    "## 3. SQLite Database Operations\n",
    "\n",
    "This section contains all database-related functions for:\n",
    "- Creating the database and table\n",
    "- Storing books\n",
    "- Retrieving and displaying books\n",
    "- Clearing the database"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2567caec",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Database will be stored at: c:\\Users\\karthik chilumula\\books_app\\books.db\n"
     ]
    }
   ],
   "source": [
    "DB_PATH = os.path.join(os.getcwd(), 'books.db')\n",
    "print(f\"Database will be stored at: {DB_PATH}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b0e8e73d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Database functions defined\n"
     ]
    }
   ],
   "source": [
    "def create_database() -> sqlite3.Connection:\n",
    "    \"\"\"\n",
    "    Create SQLite database and books table.\n",
    "    \n",
    "    Creates a new database file (or connects to existing one) and\n",
    "    ensures the 'books' table exists with the proper schema.\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    sqlite3.Connection\n",
    "        Active database connection object\n",
    "    \n",
    "    Table Schema:\n",
    "    -------------\n",
    "    - id: INTEGER PRIMARY KEY AUTOINCREMENT (auto-generated unique ID)\n",
    "    - title: TEXT NOT NULL (book title)\n",
    "    - author: TEXT NOT NULL (author name)\n",
    "    - publication_year: INTEGER (year of publication)\n",
    "    \"\"\"\n",
    "    \n",
    "    conn = sqlite3.connect(DB_PATH)\n",
    "    cursor = conn.cursor()\n",
    "    \n",
    "    cursor.execute('''\n",
    "        CREATE TABLE IF NOT EXISTS books (\n",
    "            id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
    "            title TEXT NOT NULL,\n",
    "            author TEXT NOT NULL,\n",
    "            publication_year INTEGER\n",
    "        )\n",
    "    ''')\n",
    "\n",
    "    conn.commit()\n",
    "    return conn\n",
    "\n",
    "\n",
    "def clear_database(conn: sqlite3.Connection):\n",
    "    \"\"\"\n",
    "    Clear all books from the database.\n",
    "    \n",
    "    Removes all records from the books table while keeping\n",
    "    the table structure intact.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    conn : sqlite3.Connection\n",
    "        Active database connection\n",
    "    \"\"\"\n",
    "    cursor = conn.cursor()\n",
    "    \n",
    "    cursor.execute('DELETE FROM books')\n",
    "    conn.commit()\n",
    "\n",
    "\n",
    "def store_books(conn: sqlite3.Connection, books: List[Dict]):\n",
    "    \"\"\"\n",
    "    Store books in the SQLite database.\n",
    "    \n",
    "    Inserts each book from the list into the database.\n",
    "    Uses parameterized queries to prevent SQL injection.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    conn : sqlite3.Connection\n",
    "        Active database connection\n",
    "    books : List[Dict]\n",
    "        List of book dictionaries with keys: title, author, publication_year\n",
    "    \"\"\"\n",
    "    cursor = conn.cursor()\n",
    "    \n",
    "    for book in books:\n",
    "        cursor.execute('''\n",
    "            INSERT INTO books (title, author, publication_year)\n",
    "            VALUES (?, ?, ?)\n",
    "        ''', (book.get('title'), book.get('author'), book.get('publication_year')))\n",
    "    \n",
    "    # Commit all inserts at once for efficiency\n",
    "    conn.commit()\n",
    "    print(f\"✓ Stored {len(books)} books in the database.\")\n",
    "\n",
    "\n",
    "def display_books(conn: sqlite3.Connection, limit: int = None):\n",
    "    \"\"\"\n",
    "    Retrieve and display all books from the database in a formatted table.\n",
    "    \n",
    "    Fetches books from the database and prints them in a nicely\n",
    "    formatted ASCII table with aligned columns.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    conn : sqlite3.Connection\n",
    "        Active database connection\n",
    "    limit : int, optional\n",
    "        Maximum number of books to display (default: None = all books)\n",
    "    \"\"\"\n",
    "    cursor = conn.cursor()\n",
    "    \n",
    "    # Execute query with optional LIMIT clause\n",
    "    if limit:\n",
    "        cursor.execute('SELECT id, title, author, publication_year FROM books LIMIT ?', (limit,))\n",
    "    else:\n",
    "        cursor.execute('SELECT id, title, author, publication_year FROM books')\n",
    "    \n",
    "    books = cursor.fetchall()\n",
    "    \n",
    "    # Print formatted table header\n",
    "    print(\"\\n\" + \"=\" * 70)\n",
    "    print(f\"{'ID':<5} {'Title':<30} {'Author':<22} {'Year':<6}\")\n",
    "    print(\"=\" * 70)\n",
    "    \n",
    "    # Print each book with truncated strings for alignment\n",
    "    for book in books:\n",
    "        # Truncate long titles and authors to fit column width\n",
    "        title = book[1][:28] + \"..\" if len(book[1]) > 30 else book[1]\n",
    "        author = book[2][:20] + \"..\" if len(book[2]) > 22 else book[2]\n",
    "        print(f\"{book[0]:<5} {title:<30} {author:<22} {book[3]:<6}\")\n",
    "    \n",
    "    print(\"=\" * 70)\n",
    "    \n",
    "    # Get and display total count\n",
    "    cursor.execute('SELECT COUNT(*) FROM books')\n",
    "    total = cursor.fetchone()[0]\n",
    "    \n",
    "    if limit and total > limit:\n",
    "        print(f\"Showing {limit} of {total} books\")\n",
    "    else:\n",
    "        print(f\"Total: {total} books\")\n",
    "\n",
    "\n",
    "def get_all_books(conn: sqlite3.Connection) -> List[Dict]:\n",
    "    \"\"\"\n",
    "    Get all books as a list of dictionaries.\n",
    "    \n",
    "    Fetches all books from the database and converts them\n",
    "    from tuple format to dictionary format.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    conn : sqlite3.Connection\n",
    "        Active database connection\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    List[Dict]\n",
    "        List of book dictionaries with keys: id, title, author, publication_year\n",
    "    \"\"\"\n",
    "    cursor = conn.cursor()\n",
    "    cursor.execute('SELECT id, title, author, publication_year FROM books')\n",
    "    books = cursor.fetchall()\n",
    "    \n",
    "    # Convert tuples to dictionaries for easier use\n",
    "    return [\n",
    "        {\"id\": b[0], \"title\": b[1], \"author\": b[2], \"publication_year\": b[3]}\n",
    "        for b in books\n",
    "    ]\n",
    "\n",
    "print(\"✓ Database functions defined\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5a371033",
   "metadata": {},
   "source": [
    "## 4. API Client\n",
    "\n",
    "A simple HTTP client function to fetch book data from the REST API using the `requests` library."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0066dc4c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ API client configured for: http://127.0.0.1:5000/books\n"
     ]
    }
   ],
   "source": [
    "def fetch_books_from_api(api_url: str) -> List[Dict]:\n",
    "    \"\"\"\n",
    "    Fetch books data from external REST API.\n",
    "    \n",
    "    Makes an HTTP GET request to the specified URL and parses\n",
    "    the JSON response into a list of book dictionaries.\n",
    "    \n",
    "    Parameters:\n",
    "    -----------\n",
    "    api_url : str\n",
    "        The full URL of the API endpoint (e.g., 'http://127.0.0.1:5000/books')\n",
    "    \n",
    "    Returns:\n",
    "    --------\n",
    "    List[Dict]\n",
    "        List of book dictionaries from the API, or empty list if error occurs\n",
    "    \n",
    "    Error Handling:\n",
    "    ---------------\n",
    "    - Catches all request exceptions (network errors, timeouts, etc.)\n",
    "    - Returns empty list on failure instead of raising exception\n",
    "    - Prints error message for debugging\n",
    "    \"\"\"\n",
    "    try:\n",
    "        # Make GET request with 10-second timeout\n",
    "        response = requests.get(api_url, timeout=10)\n",
    "        \n",
    "        # Raise exception for bad status codes (4xx, 5xx)\n",
    "        response.raise_for_status()\n",
    "        \n",
    "        # Parse JSON response and return\n",
    "        return response.json()\n",
    "    \n",
    "    except requests.RequestException as e:\n",
    "        # Handle any request-related errors gracefully\n",
    "        print(f\"✗ Error fetching data from API: {e}\")\n",
    "        return []\n",
    "\n",
    "# Define the API URL constant\n",
    "API_URL = \"http://127.0.0.1:5000/books\"\n",
    "print(f\"✓ API client configured for: {API_URL}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ed356329",
   "metadata": {},
   "source": [
    "## 5. Main Application Execution\n",
    "\n",
    "Now let's run the complete workflow:\n",
    "1. Start the API server in a background thread\n",
    "2. Create/connect to the SQLite database\n",
    "3. Fetch books from the API\n",
    "4. Store books in the database\n",
    "5. Display the stored books"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "18bae2ce",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "==================================================\n",
      "  📚 Books Application\n",
      "==================================================\n",
      "\n",
      "[1/4] Starting API server...\n",
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ API server running at http://127.0.0.1:5000\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# STEP 1: START THE API SERVER\n",
    "# =============================================================================\n",
    "\n",
    "print(\"=\" * 50)\n",
    "print(\"  📚 Books Application\")\n",
    "print(\"=\" * 50)\n",
    "\n",
    "# Start the Flask API server in a background thread\n",
    "# This allows us to continue executing code while the server runs\n",
    "print(\"\\n[1/4] Starting API server...\")\n",
    "start_server_thread()\n",
    "\n",
    "# Wait a moment for the server to fully start\n",
    "time.sleep(1)\n",
    "print(\"✓ API server running at http://127.0.0.1:5000\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4f5207f8",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "45e218bc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "[2/4] Setting up database...\n",
      "✓ Database ready\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# STEP 2: CREATE DATABASE CONNECTION\n",
    "# =============================================================================\n",
    "\n",
    "print(\"\\n[2/4] Setting up database...\")\n",
    "\n",
    "# Create or connect to the SQLite database\n",
    "conn = create_database()\n",
    "\n",
    "# Clear any existing data for a fresh run\n",
    "# This ensures we don't have duplicate entries from previous runs\n",
    "clear_database(conn)\n",
    "\n",
    "print(\"✓ Database ready\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c81c756d",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [14/Jan/2026 13:55:34] \"GET /books HTTP/1.1\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "[3/4] Fetching books from API...\n",
      "✓ Fetched 100 books from API\n",
      "\n",
      "Sample book data:\n",
      "  {'author': 'Toni Morrison', 'id': 1, 'publication_year': 2022, 'title': 'Waves of Change III'}\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# STEP 3: FETCH BOOKS FROM API\n",
    "# =============================================================================\n",
    "\n",
    "print(\"\\n[3/4] Fetching books from API...\")\n",
    "\n",
    "# Make HTTP request to our Flask API server\n",
    "# The server returns JSON data which is automatically parsed\n",
    "books = fetch_books_from_api(API_URL)\n",
    "\n",
    "if books:\n",
    "    print(f\"✓ Fetched {len(books)} books from API\")\n",
    "    \n",
    "    # Show a sample of the fetched data\n",
    "    print(f\"\\nSample book data:\")\n",
    "    print(f\"  {books[0]}\")\n",
    "else:\n",
    "    print(\"✗ No books fetched from API\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7c6e1efa",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "[4/4] Storing books in database...\n",
      "✓ Stored 100 books in the database.\n",
      "\n",
      "📖 Books in Database:\n",
      "\n",
      "======================================================================\n",
      "ID    Title                          Author                 Year  \n",
      "======================================================================\n",
      "1     Waves of Change III            Toni Morrison          2022  \n",
      "2     Tales of Wonder II             Hermann Hesse          2005  \n",
      "3     The Hidden Path II             Toni Morrison          1857  \n",
      "4     The Last Chapter I             Dan Brown              1937  \n",
      "5     Waves of Change I              Jane Austen            1974  \n",
      "6     Beyond the Horizon III         J.K. Rowling           1955  \n",
      "7     The Crystal Tower II           F. Scott Fitzgerald    1932  \n",
      "8     The Midnight Garden I          Virginia Woolf         1963  \n",
      "9     The Midnight Garden III        Oscar Wilde            1878  \n",
      "10    The Velvet Night III           F. Scott Fitzgerald    1953  \n",
      "11    The Frozen Lake II             George Orwell          1999  \n",
      "12    The Shattered Glass            Haruki Murakami        1873  \n",
      "13    The Empty Throne III           Virginia Woolf         1902  \n",
      "14    Secrets of the Heart II        Mark Twain             2003  \n",
      "15    Winds of Fortune I             Haruki Murakami        1889  \n",
      "16    Broken Promises II             Oscar Wilde            1875  \n",
      "17    The Silent Echo III            Stephen King           1859  \n",
      "18    The Final Hour                 J.K. Rowling           1880  \n",
      "19    Secrets of the Heart I         Virginia Woolf         2004  \n",
      "20    Depths of Despair I            Jane Austen            1959  \n",
      "======================================================================\n",
      "Showing 20 of 100 books\n",
      "\n",
      "==================================================\n",
      "  ✓ Application completed successfully!\n",
      "==================================================\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# STEP 4: STORE AND DISPLAY BOOKS\n",
    "# =============================================================================\n",
    "\n",
    "print(\"\\n[4/4] Storing books in database...\")\n",
    "\n",
    "# Insert all fetched books into the SQLite database\n",
    "store_books(conn, books)\n",
    "\n",
    "# Display the stored books in a formatted table\n",
    "# Limiting to 20 books to keep output manageable\n",
    "print(\"\\n📖 Books in Database:\")\n",
    "display_books(conn, limit=20)\n",
    "\n",
    "# Print completion message\n",
    "print(\"\\n\" + \"=\" * 50)\n",
    "print(\"  ✓ Application completed successfully!\")\n",
    "print(\"=\" * 50)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a1688ebf",
   "metadata": {},
   "source": [
    "## 6. Cleanup\n",
    "\n",
    "Close the database connection when done. This is important to prevent resource leaks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "00062dcf",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✓ Database connection closed\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# CLEANUP: Close database connection\n",
    "# =============================================================================\n",
    "\n",
    "# Always close database connections when done\n",
    "# This releases the file lock and frees resources\n",
    "conn.close()\n",
    "print(\"✓ Database connection closed\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
