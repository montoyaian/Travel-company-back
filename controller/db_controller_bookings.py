from Classes.bill import Bill
from Classes.booking import Booking
import mysql.connector

DELETE_SUCCESS = {"message": "eliminacion completa"}

connection = mysql.connector.connect(user='uluf7v2ee4qsnl5t',password='t9oXzVw4GBxRQm0VgWGm',host='bawcgrp6dvncdrpjz2lu-mysql.services.clever-cloud.com',database='bawcgrp6dvncdrpjz2lu',port='3306')
cursor = connection.cursor()
class DatabaseControllerBokings():

    """
    This class is used to connect to the database and execute queries
    """
    def insert_booking(self, booking: Booking):
        cursor = connection.cursor()
        if booking.type_flight =="standart class":
            cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE ID= %s""", (booking.id_flight,))
            flight = cursor.fetchone()
            if flight and flight[4]>=booking.cant_positions:
                if booking.type_client == "standart client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight= %s AND 
                    Type_client = 'standart client'""", (booking.id_flight,))
                    offer = cursor.fetchone()
                    if not offer:
                        discount = 0.0 
                    else:
                        discount = float(offer[2])
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE ID= %s""", (booking.id_client,))
                    client = cursor.fetchone()
                    if client:                      
                        price_position = flight[7]
                        flight_new_positions = flight[4] - booking.cant_positions
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.standart_class SET
                        Positions=%s
                        WHERE id = %s""",
                        (
                        flight_new_positions,
                        flight[0],
                        ),
                        )
                        connection.commit()
                        client_new_bookings = client[3] + 1 
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.standart_client SET
                        Bookings=%s
                        WHERE id = %s""",
                        (
                        client_new_bookings,
                        client[0],
                        ),
                        )
                        connection.commit()
                        new_cost_position = price_position - (price_position * discount/100)
                        cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.bookings(
                        Cant_positions,
                        Id_flight,
                        Id_client,
                        Type_flight,
                        Type_client,
                        Cost_position
                        ) VALUES (%s, %s, %s, %s, %s, %s )''',
                        (   
                        booking.cant_positions,
                        booking.id_flight,
                        booking.id_client,
                        booking.type_flight,
                        booking.type_client,
                        new_cost_position,
                        ))
                        connection.commit()
                        bookingj = {
                        "cant_position":booking.cant_positions,
                        "Id_flight": booking.id_flight,
                        "Id_client": booking.id_client,
                        "Type_flight": booking.type_flight,
                        "Type_client": booking.type_client,
                        "Cost_position": new_cost_position,
                        }     
                        return bookingj
                    else:
                        return{"error":"el cliente que realiza la reserva no se ha encontrado"}
                    
                elif booking.type_client == "premium client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight= %s AND 
                                Type_client = 'premium client'""", (booking.id_flight,))
                    offer = cursor.fetchone()
                    if not offer:
                        discount = 0 
                    else:
                        discount = offer[2]
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE ID= %s""", (booking.id_client,))
                    client = cursor.fetchone()
                    if client:                    
                        price_position = flight[7]
                        flight_new_positions = flight[4] - booking.cant_positions
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.standart_class SET
                        Positions=%s
                        WHERE id = %s""",
                        (
                        flight_new_positions,
                        flight[0],
                        ),
                        )
                        connection.commit()
                        client_new_bookings =client[3]+ 1
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.premium_client SET
                        Bookings=%s
                        WHERE id = %s""",
                        (
                        client_new_bookings,
                        client[0],
                        ),
                        )
                        connection.commit()
                        new_cost_position = price_position - price_position * (discount/100)
                        cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.bookings(
                        Cant_positions,
                        Id_flight,
                        Id_client,
                        Type_flight,
                        Type_client,
                        Cost_position
                        ) VALUES (%s, %s, %s, %s, %s, %s )''',
                        (   
                        booking.cant_positions,
                        booking.id_flight,
                        booking.id_client,
                        booking.type_flight,
                        booking.type_client,
                        new_cost_position,
                        )) 
                        connection.commit()  
                        bookingj = {
                        "cant_position":booking.cant_positions,
                        "Id_flight": booking.id_flight,
                        "Id_client": booking.id_client,
                        "Type_flight": booking.type_flight,
                        "Type_client": booking.type_client,
                        "Cost_position":new_cost_position,
                        }  
                        return bookingj
                    else:
                        return{"error":"el cliente que realiza la reserva no se ha encontrado"}
                else:
                    return{"error":"tipo de cliente no encontrado"}               
            else:
                return{"error":"vuelo no disponible"} 
              
        elif(booking.type_flight =="firts class"):
            cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE ID= %s""", (booking.id_flight,))
            flight = cursor.fetchone()
            if flight and flight[4]>=booking.cant_positions:
                if booking.type_client == "standart client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight= %s AND 
                    Type_client = 'standart client'""", (booking.id_flight,))
                    offer = cursor.fetchone()
                    if not offer:
                        discount = 0 
                    else:
                        discount = offer[2]
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE ID= %s""", (booking.id_client,))
                    client = cursor.fetchone()
                    if client:                    
                        price_position = flight[7]
                        flight_new_positions= flight[4] - booking.cant_positions
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                        Positions=%s
                        WHERE id = %s""",
                        (
                        flight_new_positions,
                        flight[0],
                        ),
                        )
                        connection.commit()
                        client_new_bookings = client[3] + 1
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.standart_client SET
                        Bookings=%s
                        WHERE id = %s""",
                        (
                        client_new_bookings,
                        client[0],
                        ),
                        )
                        connection.commit()
                        new_cost_position = price_position - price_position * (discount/100)
                        cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.bookings(
                        Cant_positions,
                        Id_flight,
                        Id_client,
                        Type_flight,
                        Type_client,
                        Cost_position
                        ) VALUES (%s, %s, %s, %s, %s, %s )''',
                        (   
                        booking.cant_positions,
                        booking.id_flight,
                        booking.id_client,
                        booking.type_flight,
                        booking.type_client,
                        new_cost_position,
                        ))   
                        connection.commit()
                        bookingj = {
                        "cant_position":booking.cant_positions,
                        "Id_flight": booking.id_flight,
                        "Id_client": booking.id_client,
                        "Type_flight": booking.type_flight,
                        "Type_client": booking.type_client,
                        "Cost_position":new_cost_position,
                        }        
                        return bookingj
                    else:
                        return{"error":"el cliente que realiza la reserva no se ha encontrado"}
                    
                elif booking.type_client == "premium client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight= %s AND 
                                Type_client = 'premium client'""", (booking.id_flight,))
                    offer = cursor.fetchone()
                    if not offer:
                        discount = 0 
                    else:
                        discount = offer[2]
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE ID= %s""", (booking.id_client,))
                    client = cursor.fetchone()
                    if client:                    
                        price_position = flight[7]
                        flight_new_positions = flight[4] - booking.cant_positions
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                        Positions=%s
                        WHERE id = %s""",
                        (
                        flight_new_positions,
                        flight[0],
                        ),
                        )
                        connection.commit()
                        client_new_bookings= client[3] + 1
                        cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.premium_client SET
                        Bookings=%s
                        WHERE id = %s""",
                        (
                        client_new_bookings,
                        client[0],
                        ),
                        )
                        connection.commit()
                        new_cost_position = price_position - price_position * (discount/100)
                        cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.bookings(
                        Cant_positions,
                        Id_flight,
                        Id_client,
                        Type_flight,
                        Type_client,
                        Cost_position
                        ) VALUES (%s, %s, %s, %s, %s, %s )''',
                        (   
                        booking.cant_positions,
                        booking.id_flight,
                        booking.id_client,
                        booking.type_flight,
                        booking.type_client,
                        new_cost_position,
                        ))
                        connection.commit()                        
                        bookingj = {
                        "cant_position":booking.cant_positions,
                        "Id_flight": booking.id_flight,
                        "Id_client": booking.id_client,
                        "Type_flight": booking.type_flight,
                        "Type_client": booking.type_client,
                        "Cost_position":new_cost_position,
                        }  
                        return bookingj
                    else:
                        return{"error":"el cliente que realiza la reserva no se ha encontrado"}
                else:
                    return{"error":"tipo de cliente no encontrado"}               
            else:
                return{"error":"vuelo no disponible"} 
        
        else:
            return{"error":"tipo de vuelo no encontrado"}
          
    def edit_booking(self, cant_position:int, id_booking:int):
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Bookings WHERE ID= %s""", (id_booking,))
        booking = cursor.fetchone()
        if booking:
            if booking[4] == "standart class":
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class  WHERE ID= %s""", (booking[2],))
                flight = cursor.fetchone()
                flight_old_position = flight[4] + booking[1]
                if flight_old_position > cant_position:
                    flight_new_position = flight_old_position - cant_position
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.standart_class SET
                    Positions=%s
                    WHERE id = %s""",
                    (
                    flight_new_position,
                    flight[0],
                    ),
                    )
                    print(cant_position)
                    connection.commit()
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.bookings SET
                    Cant_positions=%s
                    WHERE id = %s""",
                    (
                    cant_position,
                    booking[0],
                    ),
                    )
                    connection.commit()
                    bookingj = {
                    "Cant_position": cant_position,
                    "Id_flight": booking[2],
                    "Id_client": booking[3],
                    "Type_flight": booking[4],
                    "Type_client": booking[5],
                    "Cost_position": booking[6]
                    }  
                    return bookingj
                else:
                    return {"error": "cantidad de puestos no disponibles" }
            else:
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class  WHERE ID= %s""", (booking[2],))
                flight = cursor.fetchone()
                flight_old_position = flight[4] + booking[1]
                if flight_old_position > cant_position:
                    flight_new_position = flight_old_position - cant_position
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                    Positions=%s
                    WHERE id = %s""",
                    (
                    flight_new_position,
                    flight[0],
                    ),
                    )
                    connection.commit()
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.bookings SET
                    Cant_positions=%s
                    WHERE id = %s""",
                    (
                    cant_position,
                    booking[0],
                    ),
                    )
                    connection.commit()
                    bookingj = {
                    "Cant_position": cant_position,
                    "Id_flight": booking[2],
                    "Id_client": booking[3],
                    "Type_flight": booking[4],
                    "Type_client": booking[5],
                    "Cost_position": booking[6]
                    }  
                    return bookingj
                else:
                    return {"error": "cantidad de puestos no disponibles" }
        else:
            return{"error":"reserva no encontrada"}
    
    def delete_booking(self, id:int):
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.Bookings WHERE ID= %s""", (id,))
        booking = cursor.fetchone()
        if booking:
            if booking[4] == "standart class":
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE ID= %s""", (booking[2],))
                flight = cursor.fetchone()
                flight_new_position = flight[4] + booking[1]
                cursor.execute(
                """UPDATE bawcgrp6dvncdrpjz2lu.standart_class SET
                Positions=%s
                WHERE id = %s""",
                (
                flight_new_position,
                flight[0],
                ),
                )
                connection.commit()
                if booking[5] == "standart client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE ID= %s""", (booking[3],))
                    client = cursor.fetchone()
                    client_new_booking = client[3] - 1
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.standart_client SET
                    bookings=%s
                    WHERE id = %s""",
                    (
                    client_new_booking,
                    client[0],
                    ),
                    )
                    connection.commit()
                else:
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_client WHERE ID= %s""", (booking[3],))
                    client = cursor.fetchone()
                    client_new_booking = client[3] - 1
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.premium_client SET
                    bookings=%s
                    WHERE id = %s""",
                    (
                    client_new_booking,
                    client[0],
                    ),
                    )
                    connection.commit()
            else:
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE ID= %s""", (booking[2],))
                flight = cursor.fetchone()
                flight_old_position = flight[4] + booking[1]
                flight_new_position = flight_old_position - booking[1]
                cursor.execute(
                """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                Positions=%s
                WHERE id = %s""",
                (
                flight_new_position,
                flight[0],
                ),
                )
                connection.commit()
                cursor.execute(
                """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                Positions=%s
                WHERE id = %s""",
                (
                flight_new_position,
                flight[0],
                ),
                )
                connection.commit()
                if booking[5] == "standart client":
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE ID= %s""", (booking[3],))
                    client = cursor.fetchone()
                    client_new_booking = client[3] - 1
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.standart_client SET
                    bookings=%s
                    WHERE id = %s""",
                    (
                    client_new_booking,
                    client[0],
                    ),
                    )
                    connection.commit()
                else:
                    cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_client WHERE ID= %s""", (booking[3],))
                    client = cursor.fetchone()
                    client_new_booking = client[3] - 1
                    cursor.execute(
                    """UPDATE bawcgrp6dvncdrpjz2lu.premium_client SET
                    bookings=%s
                    WHERE id = %s""",
                    (
                    client_new_booking,
                    client[0],
                    ),
                    )
                    connection.commit()
                
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.Bookings WHERE ID= %s""", (id,))
            connection.commit()
            return DELETE_SUCCESS
        else:
            return{"error":"reserva no encontrada"}
                    
    def show_booking(self):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.bookings')
        rows = cursor.fetchall()      
        return rows 
    
    def show_bill(self, id_booking:int, payment_method:str):
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.bookings WHERE ID= %s""", (id_booking,))
        booking = cursor.fetchone() 
        if booking:
            total_cost = booking[6] * booking[1]
            bill = Bill(id_booking, total_cost, id_booking, payment_method)
            return bill.__str__()  
        else:
            return {"error": "Reserva no encontrada"}