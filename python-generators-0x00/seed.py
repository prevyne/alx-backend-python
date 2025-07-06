#!/usr/bin/python3
"""
This script sets up and seeds the ALX_prodev database.
It generates a unique user_id for each record from the CSV and includes
a workaround for the 'caching_sha2_password' authentication issue.
"""
import mysql.connector
import csv
import os
import uuid

# --- Database Connection Details ---
# IMPORTANT: Replace with your actual MySQL credentials
DB_CONFIG = {
    'user': 'Prevyne',
    'password': 'Administrator1!',
    'host': 'localhost'
}
DB_NAME = 'ALX_prodev'

def connect_db():
    """Connects to the MySQL database server."""
    try:
        config = DB_CONFIG.copy()
        # Add auth_plugin to handle authentication issues
        config['auth_plugin'] = 'mysql_native_password'
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database in MYSQL."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DB_NAME
        # Add auth_plugin to handle authentication issues
        config['auth_plugin'] = 'mysql_native_password'
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DB_NAME}': {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        cursor.execute("ALTER TABLE user_data ADD INDEX (user_id);")
        print("Table 'user_data' created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")


def insert_data(connection, data_file):
    """
    Inserts data from a CSV file into the database if the table is empty,
    generating a UUID for each user.
    """
    if not connection:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM user_data")
        if cursor.fetchone()[0] > 0:
            print("Data already exists in 'user_data'. Skipping insertion.")
            return

        with open(data_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
            
            data_to_insert = [
                (str(uuid.uuid4()), row['name'], row['email'], row['age'])
                for row in reader
            ]
            
            cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"Data from {data_file} inserted successfully.")

    except (mysql.connector.Error, FileNotFoundError, KeyError) as err:
        print(f"Error inserting data: {err}")
        connection.rollback()
    finally:
        cursor.close()