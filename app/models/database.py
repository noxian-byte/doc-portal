import mysql.connector
from flask import current_app
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
        """ Close the database connection and cursor """
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("Connection Closed")

    def fetch_one(self, query, params):
        """ Execute query and return one result """
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        """ Execute query and return all results """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params=()):
        """ Execute a query that modifies data (INSERT, UPDATE, DELETE) """
        self.cursor.execute(query, params)
        self.db.commit()

db = Database()

# optional
def init_app(app):
    """ Initialize the app with a custom database connection """
    @app.teardown_appcontext
    def close_db(error):
        """ Close the database connection after each request """
        db.close_connection()
