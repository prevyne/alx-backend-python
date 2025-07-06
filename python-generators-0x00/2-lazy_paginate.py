#!/usr/bin/python3
"""
This script demonstrates lazy loading of paginated data using a generator.
"""
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a specific 'page' of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    A generator that lazily fetches user pages one by one.
    """
    offset = 0
    # This single loop continues as long as a page with data is returned
    while True:
        # Fetch the next page of data
        page = paginate_users(page_size, offset)
        
        # If the page is empty, there's no more data to fetch.
        if not page:
            break
            
        # Yield the current page
        yield page
        
        # Increment the offset to get the next page in the next iteration
        offset += page_size