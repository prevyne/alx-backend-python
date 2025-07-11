import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to handle database connection management.
    It opens a connection, passes it to the function, and ensures it's closed.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            # Pass the connection object as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            if conn:
                conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a single user by their ID.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
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
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    conn.commit()
    conn.close()

    user = get_user_by_id(user_id=1)
    print(user)