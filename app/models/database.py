import mysql.connector
from app.config import Config

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        self.cursor = self.db.cursor()

    def close_connection(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("Connection Closed")

    def fetch_one(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.db.commit()

db = Database()