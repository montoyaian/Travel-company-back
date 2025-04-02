from fastapi import HTTPException
import pymysql
from controller.fligh_controller import bd_controller_flight
from database.config import DATABASE_CONFIG
from Classes.supplier import Supplier
from database.db_utils import DatabaseUtils
from utils.standard_response import standard_response

class DatabaseControllerSupplier:
    """
    This class is used to manage suppliers in the database.
    """
    def __init__(self):
        self.db_utils = DatabaseUtils()
        self.flighs_controller = bd_controller_flight.DatabaseControllerFlight()
      
    def insert_supplier(self, supplier: Supplier):
        query = f"""INSERT INTO railway.supplier(
                Name,
                Contact,
                Description
            ) VALUES (%s, %s, %s)"""
        params= (
                supplier.name,
                supplier.contact,
                supplier.description,
            )
        self.db_utils.execute_query(query, params)
        supplierj = {
            "name": supplier.name,
            "contact": supplier.contact,
            "Description": supplier.description,
        }
        return standard_response(
            "Proveedor agregado exitosamente", supplierj, 200
        )

    def edit_supplier(self, supplier: Supplier):
        query ="""SELECT * FROM railway.supplier WHERE ID = %s"""
        params = (supplier.id,)
        result = self.db_utils.execute_query(query, params)
        if not result:
            return {"error": "proveedor no encontrado"}

        query = """UPDATE railway.supplier SET 
                    Name = %s,
                    Contact = %s,
                    Description = %s
                WHERE ID = %s"""
        params = (
                supplier.name,
                supplier.contact,
                supplier.description,
                supplier.id,
            )
    
        self.db_utils.execute_query(query, params)
        supplierj = {
            "id": supplier.id,
            "name": supplier.name,
            "contact": supplier.contact,
            "Description": supplier.description,
        }
        return standard_response(
            "Proveedor editado exitosamente", supplierj, 200)

    def delete_supplier(self, id: int):

        query = """SELECT * FROM railway.supplier WHERE id = %s"""
        params = (id,)
        result = self.db_utils.execute_query(query, params) 
        if result:

            query=f"""DELETE FROM railway.supplier WHERE id = %s"""
            params = (id,)
            self.db_utils.execute_query(query, params)
            query=  """DELETE FROM railway.first_class WHERE ID_agency = %s"""
            params = (id,)
            self.db_utils.execute_query(query, params)
            query=  """DELETE FROM railway.standart_class WHERE ID_agency = %s"""
            params = (id,)
            self.db_utils.execute_query(query, params)
            return standard_response(
                "Proveedor eliminado exitosamente", None, 200
            )
        else:
            raise HTTPException(status_code=400, detail="El ID no está registrado")

    def show_supplier_name(self):
        query = """SELECT ID, Name FROM railway.supplier"""
        result = self.db_utils.execute_query(query)
        rowsj = [{"id": row[0], "name": row[1]} for row in result]
        return rowsj

    def show_supplier(self, id: str):
        if id == "all":
            query = """SELECT * FROM railway.supplier"""
            result = self.db_utils.execute_query(query)
            rowsj = [{
                "id": row[0],
                "name": row[1],
                "contact": row[2],
                "Description": row[3],
            } for row in result]
            return rowsj
        
        try:
            id = int(id)
            query = """SELECT * FROM railway.supplier WHERE id = %s"""
            params = (id,)
            result = self.db_utils.execute_query(query, params)
            if result:
                row = result[0]
                rowj = {
                    "id": row[0],
                    "name": row[1],
                    "contact": row[2],
                    "Description": row[3],
                }
                return rowj
            else:
                return {"message": "Proveedor no encontrado"}
        except ValueError:
            return {"message": "ID no válido"}