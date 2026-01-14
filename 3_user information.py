import csv
import sqlite3
import os


def import_csv_to_sqlite(csv_filename, db_filename="users.db", table_name="users"):
    """
    Read user data from a CSV file and store it in an SQLite database.
    Expected CSV columns: name, email
    """
    conn = None

    try:
        # Connect to or create the SQLite database
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        print(f"Connected to database: {db_filename}")

        # Create the users table if it does not exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        """)
        print(f"Table '{table_name}' is ready.")

        # Open and read the CSV file
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Skip the header row
            header = next(reader, None)
            print(f"Reading CSV file: {csv_filename}")
            print(f"Detected columns: {header}")

            insert_query = f"""
                INSERT INTO {table_name} (name, email)
                VALUES (?, ?)
            """

            # Insert each row into the database
            for row in reader:
                try:
                    cursor.execute(insert_query, row)
                except sqlite3.IntegrityError:
                    print(f"Skipping duplicate or invalid entry: {row}")
                except Exception as e:
                    print(f"Error processing row {row}: {e}")

        # Commit changes
        conn.commit()
        print(f"Data successfully imported into '{db_filename}'.")

    except FileNotFoundError:
        print(f"CSV file not found: {csv_filename}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    CSV_FILE = "users.csv"
    DB_FILE = "users.db"

    # Import CSV data into SQLite
    import_csv_to_sqlite(CSV_FILE, DB_FILE)

    # Optional verification
    if os.path.exists(DB_FILE):
        print("\nVerifying stored users:")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        for user in cursor.fetchall():
            print(user)

        conn.close()
