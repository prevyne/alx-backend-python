#!/usr/bin/python3
"""
This script provides functions to stream and process user data in batches.
"""
seed = __import__('seed')

def stream_users_in_batches(batch_size=50):
    """
    A generator that fetches users from the database in batches.
    """
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        while True:
            # Fetch a specific number of rows
            batch = cursor.fetchmany(batch_size)
            # If the batch is empty, we've reached the end of the data
            if not batch:
                break
            # Yield the entire batch (a list of dictionaries)
            yield batch

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size=50):
    """
    Processes user data in batches, filtering for users over 25.
    """
    # Get the generator
    user_batches = stream_users_in_batches(batch_size)
    
    # Loop 1: Iterate through each batch yielded by the generator
    for batch in user_batches:
        # Loop 2: Iterate through each user in the batch
        for user in batch:
            if user['age'] > 25:
                print(user)