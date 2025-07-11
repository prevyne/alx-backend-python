import asyncio
import aiosqlite

async def setup_database(db_name):
    """A helper function to create and populate the database for the demo."""
    async with aiosqlite.connect(db_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        users = [('Alice', 30), ('Bob', 25), ('Charlie', 45), ('David', 50)]
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        await db.commit()

async def async_fetch_users(db_name):
    """Fetches all users from the database asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(db_name):
    """Fetches users older than 40 from the database asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Executes both fetch queries concurrently and prints the results."""
    db_name = ":memory:"
    await setup_database(db_name) # Prepare the database
    
    all_users, older_users = await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )

    print("All Users:", all_users)
    print("Users Older Than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())