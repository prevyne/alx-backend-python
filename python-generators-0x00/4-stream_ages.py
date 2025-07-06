#!/usr/bin/python3
"""
This script calculates the average age of users in a memory-efficient way.
"""
seed = __import__('seed')

def stream_user_ages():
    """
    A generator that yields user ages one by one from the database.
    """
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return
        
        # This cursor fetches rows as tuples, which is slightly more efficient
        # since we only need one value.
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")
        
        # Loop 1: Iterate over the cursor, fetching one age at a time.
        for row in cursor:
            yield row[0]

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of all users using the generator.
    """
    total_age = 0
    user_count = 0
    
    # Get the generator that streams ages
    age_generator = stream_user_ages()
    
    # Loop 2: Iterate through each age yielded by the generator.
    for age in age_generator:
        total_age += age
        user_count += 1
        
    # Avoid division by zero if the database is empty
    if user_count == 0:
        average_age = 0
    else:
        average_age = total_age / user_count
        
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()