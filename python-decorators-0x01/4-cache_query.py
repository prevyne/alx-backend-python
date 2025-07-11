import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle database connection management."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    """
    A decorator to cache the results of a database query based on the query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or args[0]
        if query in query_cache:
            print("Fetching result from cache...")
            return query_cache[query]

        print("Executing query and caching the result...")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database, utilizing a cache.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    # Simulate a delay to show the benefit of caching
    time.sleep(1)
    return cursor.fetchall()

# Example usage
if __name__ == '__main__':
    # Setup a dummy database for testing
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    conn.commit()
    conn.close()
    
    start_time = time.time()
    # First call will execute the query and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"First call took: {time.time() - start_time:.2f}s")
    print("Users:", users)
    
    start_time = time.time()
    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Second call took: {time.time() - start_time:.2f}s")
    print("Users again:", users_again)