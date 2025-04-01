import pymysql

class DatabaseConnection:
    def __init__(self, host, user, password, database, port):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port,
        }
        self.connection = None

    def create_connection(self):
        try:
            self.connection = pymysql.connect(**self.config)
            print("Connection to MySQL DB successful")
        except pymysql.MySQLError as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")