from fastapi import HTTPException
import pymysql
from controller.offers_controller.offer_utils import findflight
from database.config import DATABASE_CONFIG
from Classes.offers import Offer
from database.db_utils import DatabaseUtils
from utils.standard_response import standard_response


class OffersController:
    def __init__(self):
        self.db_utils = DatabaseUtils()

    def insert_offer(self, offer: Offer):
        flightType = "standart_class" if offer.flight_type == "standartclass" else "first_class"
        result = findflight(offer.id_flight, self.db_utils, flightType)
        
        if result:
            query = """INSERT INTO railway.offers(
                Id_flight,
                Discount,
                Customer_type,
                Flight_type
            ) VALUES (%s, %s, %s, %s)"""
            params = (offer.id_flight, offer.discount, offer.customer_type, offer.flight_type)
            self.db_utils.execute_query(query, params)
            
            offerj = {
                "Id_flight": offer.id_flight,
                "Discount": offer.discount,
                "Customer_type": offer.customer_type,
                "Flight_type": offer.flight_type,
            }
            return standard_response("Oferta insertada exitosamente", offerj)
        else:
            raise HTTPException(status_code=400, detail="El vuelo asignado no se ha encontrado")

    def edit_offer(self, offer: Offer):
        query = "SELECT * FROM railway.offers WHERE id = %s"
        params = (offer.id,)
        result = self.db_utils.execute_query(query, params)
        
        if result:
            flightType = "standart_class" if offer.flight_type == "standartclass" else "first_class"
            result = findflight(offer.id_flight, self.db_utils, flightType)
            
            if result:
                query = """UPDATE railway.offers SET
                    Id_flight = %s,
                    Discount = %s,
                    Customer_type = %s,
                    Flight_type = %s
                    WHERE id = %s"""
                params = (offer.id_flight, offer.discount, offer.customer_type, offer.flight_type, offer.id)
                self.db_utils.execute_query(query, params)
                
                offerj = {
                    "ID": offer.id,
                    "Id_flight": offer.id_flight,
                    "Discount": offer.discount,
                    "Customer_type": offer.customer_type,
                    "Flight_type": offer.flight_type,
                }
                return standard_response("Oferta actualizada exitosamente", offerj)
            else:
                raise HTTPException(status_code=400, detail="El vuelo asignado no se ha encontrado")
        else:
            raise HTTPException(status_code=400, detail="No se ha encontrado la oferta")

    def delete_offer(self, id: int):
        query = "SELECT * FROM railway.offers WHERE id = %s"
        params = (id,)
        result = self.db_utils.execute_query(query, params)
        
        if result:
            query = "DELETE FROM railway.offers WHERE id = %s"
            params = (id,)
            self.db_utils.execute_query(query, params)
            return standard_response("Oferta eliminada exitosamente")
        else:
            raise HTTPException(status_code=400, detail="Oferta no encontrada")

    def show_offer(self, id: str):
        if id == "all":
            query = "SELECT * FROM railway.offers"
            rows = self.db_utils.fetch_all(query)
            
            rowsj = []
            for i in rows:
                rowj = {
                    "id": i[0],
                    "Id_flight": i[1],
                    "Discount": i[2],
                    "Customer_type": i[3],
                    "Flight_type": i[4],
                }
                rowsj.append(rowj)
            
            return standard_response("Listado de ofertas", rowsj)
        else:
            try:
                query = "SELECT * FROM railway.offers WHERE ID = %s"
                params = (id,)
                rows = self.db_utils.fetch_all(query, params)
                
                rowj = {
                    "id": rows[0],
                    "Id_flight": rows[1],
                    "Discount": rows[2],
                    "Customer_type": rows[3],
                    "Flight_type": rows[4],
                }
                return standard_response("Oferta encontrada", rowj)
            except:
                raise HTTPException(status_code=400, detail="No se ha encontrado la oferta")
