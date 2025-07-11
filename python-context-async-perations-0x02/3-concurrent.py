import asyncio
import aiosqlite

async def setup_database(db_name):
    """A helper function to create and populate the database for the demo."""
    async with aiosqlite.connect(db_name) as db:
        # Drop the table if it exists to ensure a clean state on each run
        await db.execute('DROP TABLE IF EXISTS users')
        await db.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        users = [('Alice', 30), ('Bob', 25), ('Charlie', 45), ('David', 50)]
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        await db.commit()

async def async_fetch_users():
    """Fetches all users from the database asynchronously."""
    db_name = "main.db"
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetches users older than 40 from the database asynchronously."""
    db_name = "main.db"
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Executes both fetch queries concurrently and prints the results."""
    db_name = "main.db"
    # Set up a clean database for this run
    await setup_database(db_name) 
    
    # Use asyncio.gather to run the functions concurrently
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()
    
    results = await asyncio.gather(all_users_task, older_users_task)

    print("All Users:", results[0])
    print("Users Older Than 40:", results[1])

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())