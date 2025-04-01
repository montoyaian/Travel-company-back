import pymysql
from database.config import DATABASE_CONFIG

class DatabaseUtils:
    def __init__(self):
        self.connection = pymysql.connect(**DATABASE_CONFIG)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchall() if cursor else []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchone() if cursor else None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()