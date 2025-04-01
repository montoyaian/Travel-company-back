from fastapi import HTTPException
from Classes.standart_client import Standardclient
from Classes.premium_client import PremiumClient
from Classes.Admins import Admins
from database.db_utils import DatabaseUtils
from fastapi.encoders import jsonable_encoder
from .clients_utils import UserUtils
import jwt
from models.client_model import *
from dotenv import load_dotenv
import os
from utils.standard_response import standard_response

class DatabaseControllerClient:
    def __init__(self):
        self.db_utils = DatabaseUtils()
    def login(self, login_item: loginModel):
        try:
            SECRET_KEY = os.getenv("SECRET_KEY")
            ALGORITHM = os.getenv("ALGORITHM")

            rows = self.db_utils.fetch_all("SELECT * FROM railway.standart_client")
            data = jsonable_encoder(login_item)
            for i in rows:
                if (i[1] == data["name"]) and (i[5] == data["password"]):
                    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                    return standard_response(
                        "Inicio de sesión exitoso", {"token": encoded_jwt, "user_role": "user"}, 200
                    )

            rows = self.db_utils.fetch_all("SELECT * FROM railway.premium_client")
            for i in rows:
                if (i[1] == data["name"]) and (i[5] == data["password"]):
                    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                    return standard_response(
                        "Inicio de sesión exitoso", {"token": encoded_jwt, "user_role": "user"}, 200
                    )

            for i in Admins:
                if (i["name"] == data["name"]) and (i["password"] == data["password"]):
                    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                    return standard_response(
                        "Inicio de sesión exitoso", {"token": encoded_jwt, "user_role": "admin"}, 200
                    )

            return standard_response("Inicio de sesión fallido", None, 401)

        except Exception as e:
            return standard_response(f"Error en login: {str(e)}", None, 500)

    def insert_client(self, client: Standardclient or PremiumClient):   
        try:
            table_name = (
                "standart_client" if isinstance(client, Standardclient) else "premium_client"
            )
            query = f"""
                INSERT INTO railway.{table_name} (
                    Name, Contact, Bookings, Email, Password
                ) VALUES (%s, %s, %s, %s, %s)
            """
            params = (client.name, client.contact, 0, client.email, client.password)
            self.db_utils.execute_query(query, params)

            return standard_response(
                "Cliente insertado exitosamente",
                {
                    "name": client.name,
                    "contact": client.contact,
                    "bookings": 0,
                    "email": client.email,
                },
                201,
            )
        except Exception as e:
            return standard_response(f"Error al insertar cliente: {str(e)}", None, 401)

    def edit_client(self, client):
        
        if UserUtils.check_user_by_id(client.id):
            table_name = (
                "standart_client" if isinstance(client, Standardclient) else "premium_client"
            )
            query = f"""
                UPDATE railway.{table_name} SET
                    Name = %s, Contact = %s, Email = %s, Password = %s
                WHERE ID = %s
            """
            params = (client.name, client.contact, client.email, client.password, client.id)
            result = self.db_utils.execute_query(query, params)
            return standard_response(
                "Cliente actualizado exitosamente",
                {
                    "name": client.name,
                    "contact": client.contact,
                    "email": client.email,
                },
                400,
            )
     
        else:
            raise HTTPException(status_code=400, detail="El id no esta registrado")

    def delete_client(self, id: int, client_type: str):
        if not UserUtils.check_user_by_id(id):
            raise HTTPException(status_code=400, detail="El ID no está registrado")

        client_type = client_type.lower()
        if client_type not in ["premium_client", "standart_client"]:
            raise HTTPException(status_code=400, detail="Tipo de cliente no válido")

        table_name = "premium_client" if client_type == "premium client" else "standart_client"

        query = f"DELETE FROM railway.{table_name} WHERE ID = %s"
        result = self.db_utils.execute_query(query, (id,))

        if result:
            return standard_response(
                f"Cliente {client_type} eliminado exitosamente", None, 200
            )
        else:
            raise HTTPException(status_code=404, detail="No se pudo eliminar el cliente")

    def show_client(self, table_name: str, id: str):
        try:
            if table_name == "all":
                query = "SELECT * FROM railway.standart_client UNION SELECT * FROM railway.premium_client"
                rows = self.db_utils.fetch_all(query)
            else:
                query = f"SELECT * FROM railway.{table_name} WHERE id = %s" if id != "all" else f"SELECT * FROM railway.{table_name}"
                rows = self.db_utils.fetch_all(query, (id,) if id != "all" else None)
                if not rows:
                    raise HTTPException(status_code=400, detail="El id no esta registrado")
    
            rowsj = [
                {
                    "id": i[0],
                    "name": i[1],
                    "contact": i[2],
                    "bookings": i[3],
                    "email": i[4],
                }
                for i in rows
            ]
            return standard_response("Clientes obtenidos exitosamente", rowsj, 200)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error al obtener clientes: {str(e)}"
            )

    def premium_clients(self):
        try:
            self.db_utils.execute_query(
                """INSERT INTO railway.premium_client (Name, Contact, Bookings, Email, Password)
                   SELECT Name, Contact, Bookings, Email, Password
                   FROM railway.standart_client WHERE Bookings >= %s""",
                (4,),
            )
            self.db_utils.execute_query(
                "DELETE FROM railway.standart_client WHERE Bookings >= %s", (4,)
            )

            self.db_utils.execute_query(
                """INSERT INTO railway.standart_client (Name, Contact, Bookings, Email, Password)
                   SELECT Name, Contact, Bookings, Email, Password
                   FROM railway.premium_client WHERE Bookings < %s""",
                (4,),
            )
            self.db_utils.execute_query(
                "DELETE FROM railway.premium_client WHERE Bookings < %s", (4,)
            )

            rows = self.db_utils.fetch_all("SELECT * FROM railway.premium_client")
            rowsj = [
                {"id": i[0], "name": i[1], "contact": i[2], "Description": i[3]}
                for i in rows
            ]
            return standard_response("Clientes premium actualizados exitosamente", rowsj, 200)
        except Exception as e:
            return standard_response(f"Error al actualizar clientes premium: {str(e)}", None, 500)