import pymysql
from config import DATABASE_CONFIG

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS standart_client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact BIGINT,
    bookings INT DEFAULT 0,
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS premium_client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact BIGINT,
    bookings INT DEFAULT 0,
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS standart_class (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(255),
    destination VARCHAR(255),
    date DATE,
    positions INT,
    hour TIME,
    id_agency INT,
    standart_cost FLOAT
);

CREATE TABLE IF NOT EXISTS first_class (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(255),
    destination VARCHAR(255),
    date DATE,
    positions INT,
    hour TIME,
    id_agency INT,
    premium_cost FLOAT
);

CREATE TABLE IF NOT EXISTS supplier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact BIGINT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_flight INT,
    discount INT,
    customer_type VARCHAR(255),
    flight_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cant_positions INT,
    id_flight INT,
    id_client INT,
    type_flight VARCHAR(255),
    type_client VARCHAR(255),
    cost_position FLOAT
);

CREATE TABLE IF NOT EXISTS bill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_price FLOAT,
    id_booking INT,
    payment_method VARCHAR(255)
);
"""

def create_tables():
    try:
        print(DATABASE_CONFIG)
        connection = pymysql.connect(**DATABASE_CONFIG)
        print("Conexión exitosa a la base de datos")

        with connection.cursor() as cursor:
            for statement in CREATE_TABLES_SQL.split(";"):
                if statement.strip():
                    cursor.execute(statement)
            connection.commit()
            print("Tablas creadas exitosamente")

    except pymysql.MySQLError as e:
        print(f"Error al conectar o ejecutar SQL: {e}")

    finally:
        
        connection.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    create_tables()