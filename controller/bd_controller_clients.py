from Classes.standart_client import Standardclient
from Classes.premium_client import PremiumClient
from Classes.offers import Offer
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(user='uluf7v2ee4qsnl5t',password='t9oXzVw4GBxRQm0VgWGm',host='bawcgrp6dvncdrpjz2lu-mysql.services.clever-cloud.com',database='bawcgrp6dvncdrpjz2lu',port='3306')
cursor = connection.cursor()

DELETE_SUCCESS = {"message": "eliminacion completa"}
class DatabaseControllerClient():
    """
    This class is used to connect to the database and execute queries
    """
    def insert_client(self, client: Standardclient or PremiumClient):
        cursor = connection.cursor()
       
        if isinstance(client,Standardclient):
            cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.standart_client(
            Name,
            Contact,
            Bookings,
            Email
            ) VALUES (%s, %s, %s, %s )''',
            (   
            client.name,
            client.contact,
            0,
            client.email
            ))
            connection.commit()
            clientj = {
            "name": client.name,
            "contact": client.contact,
            "bookings": 0,
            "email": client.email,
            }
            return clientj

        elif isinstance(client,PremiumClient):
            cursor.execute('''INSERT INTO bawcgrp6dvncdrpjz2lu.premium_client(
            Name,
            Contact,
            Bookings,
            Email
            ) VALUES (%s, %s, %s, %s )''',
            (   
            client.name,
            client.contact,
            0,
            client.email
            ))
            connection.commit()
            
            clientj = {
            "name": client.name,
            "contact": client.contact,
            "bookings": client.bookings,
            "email": client.email,
            }
            return clientj

    def insert_offer(self, offer:Offer):
        cursor = connection.cursor()
        if offer.flight_type == "standart class":
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""",
            (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""INSERT INTO bawcgrp6dvncdrpjz2lu.Offers(
                Id_flight,
                Discount,
                Customer_type,
                Flight_type
                ) VALUES (%s, %s, %s, %s)""",
                (
                offer.id_flight,
                offer.discount,
                offer.customer_type,
                offer.flight_type
                ))
                connection.commit()
                
                offerj = {
                    "Id_flight":offer.id_flight,
                    "Discount":offer.discount,
                    "Customer_type":offer.customer_type,
                    "Flight_type":offer.flight_type
                    }
                return offerj
            else:
                return{"error": "id de vuelo no encotrado"}
            
        elif offer.flight_type == "firts class":
            cursor = connection.cursor()
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""",
            (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute(      """INSERT INTO  bawcgrp6dvncdrpjz2lu.Offers(
                Id_flight,
                Discount,
                Customer_type,
                Flight_type
                ) VALUES (%s, %s, %s, %s)""",
                (
                offer.id_flight,
                offer.discount,
                offer.customer_type,
                offer.flight_type
                ))
                connection.commit()
                
                offerj = {
                    "Id_flight":offer.id_flight,
                    "Discount":offer.discount,
                    "Customer_type":offer.customer_type,
                    "Flight_type":offer.flight_type
                    }
                return offerj
            else:
                return{"error": "id de vuelo no encotrado"} 
        else:
            return{"error": "tipo de vuelo no encotrado"}       
        
    def edit_client(self, client):
        cursor = connection.cursor()
        if isinstance(client, Standardclient):
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE id = %s""",
            (client.id,),
        )
            result = cursor.fetchone()
            if result:
                cursor.execute("""UPDATE bawcgrp6dvncdrpjz2lu.standart_client SET 
                Name = %s,
                Contact = %s,
                Email = %s
                WHERE ID = %s""",
                (
                client.name,
                client.contact,
                client.email,
                client.id
                ))
                connection.commit()
                
                clientj = {
                "name": client.name,
                "contact": client.contact,

                "email": client.email,
                }
                return clientj
            else:
                return{"error": "cliente no encontrado"}
        elif isinstance(client, PremiumClient):
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE id = %s""",
            (client.id,),
        )
            result = cursor.fetchone()
            if result:
                cursor.execute("""UPDATE bawcgrp6dvncdrpjz2lu.premium_client SET 
                Name = %s,
                Contact = %s,
                Email = %s
                WHERE ID = %s""",
                (
                client.name,
                client.contact,
                client.email,
                client.id
                ))
                connection.commit()
                
                clientj = {
                "name": client.name,
                "contact": client.contact,
                "email": client.email,
                }
                return clientj
            else:
                return{"error": "cliente no encontrado"}

    def edit_offer(self,offer:Offer):
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE id = %s""",
        (offer.id,),
        )
        result = cursor.fetchone()
        if result:
            if offer.flight_type == "standart class":
                cursor.execute(
                """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""",
                (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute("""UPDATE bawcgrp6dvncdrpjz2lu.Offers SET
                    Id_flight = %s,
                    Discount = %s,
                    Customer_type = %s,
                    Flight_type = %s
                    WHERE id = %s""",
                    (
                    offer.id_flight,
                    offer.discount,
                    offer.customer_type,
                    offer.flight_type,
                    offer.id
                    ))
                    connection.commit()
                    
                    offerj = {
                        "ID":offer.id,
                        "Id_flight":offer.id_flight,
                        "Discount":offer.discount,
                        "Customer_type":offer.customer_type,
                        "Flight_type":offer.flight_type
                        }
                    return offerj
                else:
                    return{"error": "id de vuelo no encotrado"}            
            elif offer.flight_type == "firts class":
                cursor.execute(
                """SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""",
                (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute(      """UPDATE bawcgrp6dvncdrpjz2lu.Offers SET
                    Id_flight = %s,
                    Discount = %s,
                    Customer_type = %s,
                    Flight_type = %s
                    WHERE id = %s""",
                    (
                    offer.id_flight,
                    offer.discount,
                    offer.customer_type,
                    offer.flight_type,
                    offer.id
                    ))
                    connection.commit()
                    
                    offerj = {
                        "ID":offer.id,
                        "Id_flight":offer.id_flight,
                        "Discount":offer.discount,
                        "Customer_type":offer.customer_type,
                        "Flight_type":offer.flight_type
                        }
                    return offerj
                else:
                    return{"error": "id de vuelo no encotrado"} 
            else:
                return{"error": "tipo de vuelo no encotrado"}            
        else:
            return{"error": "reserva no encontrada"}  
                   
    def delete_client(self, id: int, client_type: str):
        """
        Delete a client from database
        """
        cursor = connection.cursor()
        client_type.lower()
        if (client_type == "premium client"):
            cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE ID = %s """,(id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.premium_client  WHERE id = %s""", (id,))
                connection.commit()
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.bookings WHERE Id_client = %s AND Type_client = 'premium client' """,(id,))
                rows = cursor.fetchall()
                for  booking in rows:  
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
                    else:
                        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE ID= %s""", (booking[2],))
                        flight = cursor.fetchone()
                        flight_new_position = flight[4] + booking[1]
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
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.bookings  WHERE id_client = %s AND Type_client = 'premium client'""", (id,))
                connection.commit()
                
                return DELETE_SUCCESS
            else:
                return{"error":"cliente no encontrado"}
                            
        elif (client_type == "standart client"):
            cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE ID = %s """,(id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE id = %s""", (id,))
                connection.commit()
                cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.bookings WHERE Id_client = %s AND Type_client = 'standart client' """,(id,))
                rows = cursor.fetchall()
                for  booking in rows:  
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
                    else:
                        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE ID= %s""", (booking[2],))
                        flight = cursor.fetchone()
                        flight_new_position = flight[4] + booking[1]
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
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.bookings  WHERE Id_client = %s AND Type_client = 'standart client'""", (id,))
                connection.commit()
                
                return DELETE_SUCCESS
            else:
                return{"error":"cliente no encontrado"}
        else:
            return {"error":"cliente no encontrado"}
        
    def delete_offer(self, id:int):
        cursor = connection.cursor()
        """
        Delete a offer from database
        """
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE id = %s""",
        (id,),
        )
        result = cursor.fetchone()
        if result:
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.Offers  WHERE id = %s""", (id,))
            connection.commit()
            
            return DELETE_SUCCESS   
        else:
            return {"error":"oferta no encontrada"} 

    def show_client(self, table_name:str, id: str):
        cursor = connection.cursor()
        try:
            if table_name == "all":
                cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client')
                rows = cursor.fetchall()
                cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client')
                rows += cursor.fetchall()
                rowsj=[]
                for i in rows:
                    rowj ={
                    "id" : i[0],
                    "name": i[1],
                    "contact": i[2],
                    "Description": i[3],
                    }
                    rowsj.append(rowj)
    
                return rowsj
            else:
                if id == "all":
                    cursor.execute(
                        '''SELECT * FROM bawcgrp6dvncdrpjz2lu.{}'''.format(table_name))
                    rows = cursor.fetchall()
                    rowsj=[]
                    for i in rows:
                        rowj ={
                        "id" : i[0],
                        "name": i[1],
                        "contact": i[2],
                        "Description": i[3],
                        }
                        rowsj.append(rowj)
    
                    return rowsj

                else:
                    cursor.execute(
                        '''SELECT * FROM bawcgrp6dvncdrpjz2lu.{} WHERE id = {}'''.format(table_name, id))
                    rows = cursor.fetchall()
                    rowj = {
                        "id": rows[0][0],
                        "name": rows[0][1],
                        "contact": rows[0][2],
                        "Description": rows[0][3]
                    }
                    return rowj           
        except:
            return {"error": "datos no encontrados"}     

    def show_offer(self,id:str):
        cursor = connection.cursor()
        if id == "all":
            cursor.execute(
                '''SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers''')
            rows = cursor.fetchall()
            rowsj=[]
            for i in rows:
                rowj ={
                "id" : i[0],
                "name": i[1],
                "contact": i[2],
                "Description": i[3],
                }
                rowsj.append(rowj)
    
            return rowsj
        else:
            try:
                cursor.execute(
                '''SELECT * FROM bawcgrp6dvncdrpjz2lu.Offers WHERE id = {}'''.format(id))
                rows = cursor.fetchone()
                rowj = {
                "id": rows[0][0],
                "name": rows[0][1],
                "contact": rows[0][2],
                "Description": rows[0][3]
                }
                return rowj
            except:
                {"message" : "datos no validos"}
        
        
        
        
    def premium_clients(self):
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE Bookings >= %s""",
        (4,),
        )
        for row in cursor.fetchall():
            cursor.execute(
            """INSERT INTO  bawcgrp6dvncdrpjz2lu.premium_client(
            Name,
            Contact,
            Bookings,
            Email
            ) VALUES (%s, %s, %s, %s )""",
            (
            row[1], # Name
            row[2], # Contact
            row[3], # Bookings
            row[4], # Email
            ))
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.standart_client WHERE id = %s""", (row[0],))
            connection.commit()
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE Bookings  < %s""",
        (4,),
        )
        for row in cursor.fetchall():
            cursor.execute(
            """INSERT INTO  bawcgrp6dvncdrpjz2lu.standart_client(
            Name,
            Contact,
            Bookings,
            Email
            ) VALUES (%s, %s, %s, %s )""",
            (
            row[1], # Name
            row[2], # Contact
            row[3], # Bookings
            row[4], # Email
            ))
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.premium_client WHERE id = %s""", (row[0],))
            connection.commit()
        cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.premium_client')
        rows = cursor.fetchall()
        rowsj=[]
        for i in rows:
            rowj ={
            "id" : i[0],
            "name": i[1],
            "contact": i[2],
            "Description": i[3],
            }
            rowsj.append(rowj)
    
        return rowsj                   

 
        