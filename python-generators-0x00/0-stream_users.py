#!/usr/bin/python3
"""
This script makes the module itself a callable generator.
"""
import sys
seed = __import__('seed')

class StreamUsers:
    """
    A class whose instances act as a generator function to stream users.
    """
    def __call__(self):
        """
        This special method is executed when the object is called like a function.
        It contains the generator logic.
        """
        connection = None
        try:
            connection = seed.connect_to_prodev()
            if connection:
                # dictionary=True makes the cursor return rows as dictionaries
                cursor = connection.cursor(dictionary=True)
                
                cursor.execute("SELECT * FROM user_data;")

                # This loop iterates over the cursor, fetching one row at a time
                for row in cursor:
                    yield row
                    
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the connection is always closed
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

sys.modules[__name__] = StreamUsers()