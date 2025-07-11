import sqlite3

class ExecuteQuery:
    """A context manager to execute a given database query."""

    def __init__(self, query, params, db_name=':memory:'):
        """Initializes the query and its parameters."""
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None

    def __enter__(self):
        """Opens the connection and executes the query."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        # Create and populate a dummy table for the example
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        users = [('Alice', 30), ('Bob', 25), ('Charlie', 35), ('David', 45)]
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        self.conn.commit()
        
        # Execute the main query
        cursor.execute(self.query, (self.params,))
        return cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

# Example usage of the ExecuteQuery context manager
query_string = "SELECT * FROM users WHERE age > ?"
age_param = 25

with ExecuteQuery(query_string, age_param) as results:
    print(f"Users older than {age_param}:")
    for row in results:
        print(row)