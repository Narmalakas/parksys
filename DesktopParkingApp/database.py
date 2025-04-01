import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="parkingV2"
        )
        self.cursor = self.conn.cursor(dictionary=True)  # Enables fetching results as dictionaries

    def execute(self, query, params=None):
        """Executes an INSERT, UPDATE, DELETE query"""
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_one(self, query, params=None):
        """Fetches a single row from the database"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()  # Returns None if no results

    def fetch_all(self, query, params=None):
        """Fetches all rows from the database"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        """Closes the database connection"""
        self.cursor.close()
        self.conn.close()
