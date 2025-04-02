from fastapi import HTTPException
from Classes.first_class import Firstclass
from Classes.standart_class import Standartclass
from database.config import DATABASE_CONFIG
from database.db_utils import DatabaseUtils
from datetime import date
from utils.standard_response import standard_response
from .flightUtils import CheckflightInfo

class DatabaseControllerFlight:
    def __init__(self):
        self.db_utils = DatabaseUtils()

    def insert_flight(self, flight: Firstclass | Standartclass):
       
        CheckflightInfo(flight,self.db_utils)

        flightType = "first_class" if isinstance(flight, Firstclass) else "standart_class"
        cost_field = "premium_cost" if flightType == "first_class" else "standart_cost"
        
        query = f"""INSERT INTO railway.{flightType} (Origin, Destination, Date, Positions, Hour, Id_agency, {cost_field})
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (flight.origin, flight.destination, flight.date, flight.positions, flight.hour, flight.id_agency, getattr(flight, cost_field))
        
        self.db_utils.execute_query(query, params)
        return {"message": "Vuelo insertado exitosamente"}

    def edit_flight(self, flight: Firstclass | Standartclass):

        CheckflightInfo(flight,self.db_utils)
        
        flightType = "first_class" if isinstance(flight, Firstclass) else "standart_class"
        cost_field = "premium_cost" if flightType == "first_class" else "standart_cost"
        
        query = f"SELECT * FROM railway.{flightType} WHERE id = %s"
        if not self.db_utils.execute_query(query, (flight.id,)):
            return {"error": "vuelo no encontrado"}
        
        query = f"""UPDATE railway.{flightType} SET
                Origin=%s, Destination=%s, Date=%s, Positions=%s, Hour=%s, Id_agency=%s, {cost_field}=%s
                WHERE id = %s"""
        params = (flight.origin, flight.destination, flight.date, flight.positions, flight.hour, flight.id_agency, getattr(flight, cost_field), flight.id)
        
        self.db_utils.execute_query(query, params)
        return {"message": "Vuelo actualizado exitosamente"}
    
    def delete_flight(self, id: int, class_type: str):
        flightType = "first_class" if class_type.lower() == "first_class" else "standart_class"
        
        query = f"SELECT * FROM railway.{flightType} WHERE id = %s"
        if not self.db_utils.execute_query(query, (id,)):
            raise HTTPException(status_code=400, detail="Vuelo no encontrado")

        queries = [
            f"DELETE FROM railway.{flightType} WHERE id = %s",
            "DELETE FROM railway.bookings WHERE Id_flight = %s AND Type_flight = %s",
            "DELETE FROM railway.Offers WHERE Id_flight = %s"
        ]
        
        for query in queries:
            self.db_utils.execute_query(query, (id, flightType if "bookings" in query else id))
        
        return standard_response(f"Vuelo {class_type} eliminado exitosamente", None, 200)
    
    def show_flight(self, table_name: str, id: str):
        try:
            if table_name == "all":
                tables = ["first_class", "standart_class"]
            else:
                tables = [table_name]
            
            rowsj = []
            for table in tables:
                query = f"SELECT * FROM railway.{table}" + (" WHERE id = %s" if id != "all" else "")
                params = (id,) if id != "all" else ()
                rows = self.db_utils.execute_query(query, params)
                
                for i in rows:
                    rowsj.append({
                        "id": i[0],
                        "origin": i[1],
                        "destination": i[2],
                        "date": i[3],
                        "positions": i[4],
                        "hour": i[5],
                        "id_agency": i[6],
                        "cost": i[7]
                    })
            
            return rowsj if rowsj else {"message": "datos no encontrados"}
        except:
            return {"message": "datos no encontrados"}