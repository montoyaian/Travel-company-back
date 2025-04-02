from datetime import date
from fastapi import HTTPException
from Classes.first_class import Firstclass
from Classes.standart_class import Standartclass
from database.db_utils import DatabaseUtils


def CheckflightInfo(flight: Firstclass | Standartclass,db_utils:DatabaseUtils):
        query = f"SELECT * FROM railway.supplier WHERE id = %s"
        if not db_utils.execute_query(query, (flight.id_agency,)):
            raise HTTPException(status_code=400, detail="proveedor no encontrado")
        if flight.positions <= 0:
            raise HTTPException(status_code=400, detail="cantidad de puestos no aceptada")
        
        if flight.date < date.today():
            raise HTTPException(status_code=400, detail="fecha no valida")