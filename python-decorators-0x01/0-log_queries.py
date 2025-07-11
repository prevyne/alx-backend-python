import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """
    A decorator that logs the SQL query with a timestamp.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Safely determine the query string to avoid errors
        query = kwargs.get('query')
        if not query and args:
            query = args[0]

        # Format the log message with the required timestamp
        if query:
            print(f"[{datetime.now()}] Executing query: {query}")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# This block is for your own testing
if __name__ == '__main__':
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

    fetch_all_users(query="SELECT * FROM users")