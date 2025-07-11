import sqlite3
import functools

def log_queries(func):
    """
    A decorator that logs the SQL query executed by a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Safely determine the query string
        query = ""
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            query = args[0]

        # Only print the log message if a query was found
        if query:
            print(f"Executing query: {query}")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database.
    """
    # The database file should be in the same directory or provide a full path
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == '__main__':
    # Setup a dummy database for testing
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    # Add some dummy data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
        cursor.execute("INSERT INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
        conn.commit()
    conn.close()

    # Fetch users while logging the query
    print("--- Calling with keyword argument ---")
    users = fetch_all_users(query="SELECT * FROM users")
    print("Users fetched:", users)

    print("\n--- Calling with positional argument ---")
    users_pos = fetch_all_users("SELECT * FROM users WHERE id = 1")
    print("Users fetched:", users_pos)