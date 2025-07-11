import sqlite3

class DatabaseConnection:
    """A context manager for handling database connections."""

    def __init__(self, db_name=':memory:'):
        """Initializes the database connection."""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Opens the database connection."""
        print("Connecting to the database...")
        self.conn = sqlite3.connect(self.db_name)
        # Create a dummy table and insert some data for demonstration
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
        self.conn.commit()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Using the context manager to perform a query
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:", results)