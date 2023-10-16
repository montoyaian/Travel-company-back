from Classes.first_class import Firtsclass
from Classes.economic_class import Economiclass
from Classes.standart_class import Standartclass
from Classes.supplier import Supplier
import mysql.connector

DELETE_SUCCESS = {"message": "eliminacion completa"}



connection = mysql.connector.connect(user='uluf7v2ee4qsnl5t',password='t9oXzVw4GBxRQm0VgWGm',host='bawcgrp6dvncdrpjz2lu-mysql.services.clever-cloud.com',database='bawcgrp6dvncdrpjz2lu',port='3306')
cursor = connection.cursor()
class DatabaseControllerFlight():
    """
    This class is used to connect to the database and execute queries
    """

    def insert_flight(self, flight: Firtsclass or Economiclass or Standartclass):
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier WHERE id = %s""",
        (flight.id_agency,),
        )
        result = cursor.fetchone()
        if result:
            if flight.positions > 0:
                if isinstance(flight, Firtsclass):
                    cursor.execute(      """INSERT INTO  bawcgrp6dvncdrpjz2lu.firts_class(
                Origin,
                Destination,
                Date,
                Positions,
                Hour,
                Id_agency,
                Premium_cost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                flight.origin,
                flight.destination,
                flight.date,
                flight.positions,
                flight.hour,
                flight.id_agency,
                flight.premium_cost,
                ))
                    connection.commit()
                    
                    flightj = {
                    "origin": flight.origin,
                    "destination": flight.destination,
                    "date": flight.date,
                    "positions": flight.positions,
                    "hour": flight.hour,
                    "id_agency": flight.id_agency,
                    "premium_cost": flight.premium_cost
                    }
                    return flightj

            
                elif isinstance(flight, Standartclass):
                    cursor.execute(      """INSERT INTO  bawcgrp6dvncdrpjz2lu.standart_class(
                    Origin,
                    Destination,
                    Date,
                    Positions,
                    Hour,
                    Id_agency,
                    Standart_cost
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                    flight.origin,
                    flight.destination,
                    flight.date,
                    flight.positions,
                    flight.hour,
                    flight.id_agency,
                    flight.standart_cost,
                    ))
                    connection.commit()
                    
                    flightj = {
                    "origin": flight.origin,
                    "destination": flight.destination,
                    "date": flight.date,
                    "positions": flight.positions,
                    "hour": flight.hour,
                    "id_agency": flight.id_agency,
                    "standart_cost": flight.standart_cost
                    }
                    return flightj    
            else:
                return{"error": "cantidad de puestos no aceptada"}
        else:
            return{"error":"proveedor no encontrado"}
   
    def insert_supplier(self, supplier:Supplier ):
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO  bawcgrp6dvncdrpjz2lu.supplier(
        Name,
        Contact,
        Description
        ) VALUES (%s,%s, %s)""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        ))
        connection.commit()
        supplierj = {
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }

        return supplierj      


     
    def edit_supplier(self,supplier:Supplier ):
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier WHERE ID = %s""", (supplier.id,))
        result = cursor.fetchone()

        if not result :
            return {"error":"proveedor no encontrado"}

        cursor.execute("""UPDATE bawcgrp6dvncdrpjz2lu.supplier SET 
        Name = %s,
        Contact = %s,
        Description = %s
        WHERE ID = %s""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        supplier.id,
        ))
        connection.commit()
        supplierj = {
        "id": supplier.id,
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }
        return supplierj

    def edit_flight(self, flight:Standartclass or Firtsclass):
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier WHERE id = %s""",
        (flight.id_agency,),
        )
        result = cursor.fetchone()
        if result:
            if isinstance(flight, Standartclass):
                cursor.execute(
                """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""",
                (flight.id,),
            )
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.standart_class SET
                        Origin=%s,
                        Destination=%s,
                        Date= %s,
                        Positions=%s,
                        Hour=%s,
                        Id_agency=%s,
                        Standart_cost=%s
                        WHERE id = %s""",
                        (
                            flight.origin,
                            flight.destination,
                            flight.date,
                            flight.positions,
                            flight.hour,
                            flight.id_agency,
                            flight.standart_cost,
                            flight.id,
                        ),
                    )
                    connection.commit()
                    cursor.execute(
                    """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""",
                    (flight.id,),
                    )
                    updated_flight = cursor.fetchone()

                    updated_flight_dict = {
                        "id": updated_flight[0], 
                        "origin": updated_flight[1],
                        "destination": updated_flight[2],
                        "date": updated_flight[3],
                        "positions": updated_flight[4],
                        "hour": updated_flight[5],
                        "id_agency": updated_flight[6],
                        "standart_cost": updated_flight[7]
                    }
                    
                    return updated_flight_dict
                else:
                    return{"error": "vuelo no encontrado"}
           
            elif isinstance(flight, Firtsclass):
                cursor.execute(
                """SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""",
                (flight.id,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        """UPDATE bawcgrp6dvncdrpjz2lu.firts_class SET
                        Origin=%s,
                        Destination=%s,
                        Date=%s,
                        Positions=%s,
                        Hour=%s,
                        Id_agency=%s,
                        premium_cost=%s
                        WHERE id = %s""",
                        (
                        flight.origin,
                        flight.destination,
                        flight.date,
                        flight.positions,
                        flight.hour,
                        flight.id_agency,
                        flight.premium_cost,
                        flight.id,
                        ),
                    )
                    connection.commit()
                    cursor.execute(
                    """SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""",
                    (flight.id,),
                    )
                    updated_flight = cursor.fetchone()

                    updated_flight_dict = {
                        "id": updated_flight[0],  
                        "origin": updated_flight[1],
                        "destination": updated_flight[2],
                        "date": updated_flight[3],
                        "positions": updated_flight[4],
                        "hour": updated_flight[5],
                        "id_agency": updated_flight[6],
                        "premium_cost": updated_flight[7]
                    }
                    
                    return updated_flight_dict
                else:
                    return {"error": "vuelo no encontrado"}
        else:
            return{"error": "proveedor no encontrado"}
                        
    def delete_flight(self, id: int, class_type: str):
        """
        Delete a flight from database
        """
        cursor = connection.cursor()
        class_type.lower()
        if (class_type == "firts class"):
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""",
            (id,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.firts_class WHERE id = %s""", (id,))
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.bookings WHERE Id_flight= %s AND Type_flight = 'firts class'""", (id,))
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight = %s""", (id,))
                connection.commit()
                return DELETE_SUCCESS
            else:
                return{"error": "vuelo no encontrado"}            
        elif (class_type == "standart class"):
            cursor.execute(
            """SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""",
            (id,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.standart_class WHERE id = %s""", (id,))
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.bookings WHERE Id_flight= %s AND Type_flight = 'standart class'""", (id,))
                cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.Offers WHERE Id_flight = %s""", (id,))
                connection.commit()
                
                return DELETE_SUCCESS
            else:
                return{"error": "vuelo no encontrado"} 
        else:
            return {"error":"tipo de vuelo no encontrado"}
    
    def delete_supplier(self, id:int):
        """
        Delete a supplier from database
        """
        cursor = connection.cursor()
        
        cursor.execute(
        """SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier WHERE id = %s""",
        (id,),
        )
        result = cursor.fetchone()
        if result:
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.supplier  WHERE id = %s""", (id,))      
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.firts_class  WHERE ID_agency = %s""", (id,))
            cursor.execute("""DELETE FROM bawcgrp6dvncdrpjz2lu.standart_class  WHERE ID_agency = %s""", (id,))
            connection.commit()
                      
            return DELETE_SUCCESS
        else:
            return {"error":"proveedor no encontrado"}        
            
    def show_flight(self, table_name:str,id:str ):
        cursor = connection.cursor()
        try:
            if table_name == "all":
                cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.firts_class')
                rows = cursor.fetchall()
                cursor.execute('SELECT * FROM bawcgrp6dvncdrpjz2lu.standart_class')
                rows += cursor.fetchall()
                connection.commit()
                
                return rows 
            else:
                if id == "all":
                    cursor.execute(
                        '''SELECT * FROM bawcgrp6dvncdrpjz2lu.{}'''.format(table_name))
                    rows = cursor.fetchall()
                    connection.commit()
                    return rows
                else:
                    cursor.execute(
                        '''SELECT * FROM bawcgrp6dvncdrpjz2lu.{} WHERE id = {}'''.format(table_name, id))
                    rows = cursor.fetchall()
                    connection.commit()
                    return rows

        except:
            return{"message":"datos no encontrados"}

    def show_supplier(self,id:str):
        cursor = connection.cursor()
        if id == "all":
            cursor.execute(
            '''SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier''')
            rows = cursor.fetchall()
            connection.commit()
            return rows
        else:
            try:
                cursor.execute(
                '''SELECT * FROM bawcgrp6dvncdrpjz2lu.supplier WHERE id = {}'''.format(id))
                rows = cursor.fetchall()
                connection.commit()
                return rows
            except:
                {"message" : "datos no validos"}   
