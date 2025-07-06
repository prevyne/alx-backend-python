#!/usr/bin/python3
"""
This script contains a generator function to stream users from the database.
"""
seed = __import__('seed')

def stream_users():
    """
    A generator function that connects to the database and yields users
    one by one as dictionaries.
    """
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            for row in cursor:
                yield row
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()