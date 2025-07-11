import sqlite3
import functools

def log_queries(func):
    """
    A decorator that logs the SQL query executed by a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing query: {kwargs.get('query') or args[0]}")
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

# Fetch users while logging the query
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
    # Add some dummy data
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

    users = fetch_all_users(query="SELECT * FROM users")
    print("Users fetched:", users)