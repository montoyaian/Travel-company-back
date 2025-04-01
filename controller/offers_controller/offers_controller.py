import pymysql
from database.config import DATABASE_CONFIG
from Classes.offers import Offer

class OffersController:
    def insert_offer(self, offer: Offer):
        connection = pymysql.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        if offer.flight_type == "standart class":
            cursor.execute(
                """SELECT * FROM railway.standastrt_class WHERE id = %s""",
                (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute(
                    """INSERT INTO railway.Offers(
                    Id_flight,
                    Discount,
                    Customer_type,
                    Flight_type
                    ) VALUES (%s, %s, %s, %s)""",
                    (
                        offer.id_flight,
                        offer.discount,
                        offer.customer_type,
                        offer.flight_type,
                    ),
                )
                connection.commit()
                offerj = {
                    "Id_flight": offer.id_flight,
                    "Discount": offer.discount,
                    "Customer_type": offer.customer_type,
                    "Flight_type": offer.flight_type,
                }
                return offerj
            else:
                return {"error": "id de vuelo no encontrado"}

        elif offer.flight_type == "first class":
            cursor.execute(
                """SELECT * FROM railway.first_class WHERE id = %s""",
                (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute(
                    """INSERT INTO railway.Offers(
                    Id_flight,
                    Discount,
                    Customer_type,
                    Flight_type
                    ) VALUES (%s, %s, %s, %s)""",
                    (
                        offer.id_flight,
                        offer.discount,
                        offer.customer_type,
                        offer.flight_type,
                    ),
                )
                connection.commit()
                offerj = {
                    "Id_flight": offer.id_flight,
                    "Discount": offer.discount,
                    "Customer_type": offer.customer_type,
                    "Flight_type": offer.flight_type,
                }
                return offerj
            else:
                return {"error": "id de vuelo no encontrado"}
        else:
            return {"error": "tipo de vuelo no encontrado"}

    def edit_offer(self, offer: Offer):
        connection = pymysql.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """SELECT * FROM railway.Offers WHERE id = %s""",
            (offer.id,),
        )
        result = cursor.fetchone()
        if result:
            if offer.flight_type == "standart class":
                cursor.execute(
                    """SELECT * FROM railway.standart_class WHERE id = %s""",
                    (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        """UPDATE railway.Offers SET
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
                            offer.id,
                        ),
                    )
                    connection.commit()
                    offerj = {
                        "ID": offer.id,
                        "Id_flight": offer.id_flight,
                        "Discount": offer.discount,
                        "Customer_type": offer.customer_type,
                        "Flight_type": offer.flight_type,
                    }
                    return offerj
                else:
                    return {"error": "id de vuelo no encontrado"}
            elif offer.flight_type == "first class":
                cursor.execute(
                    """SELECT * FROM railway.first_class WHERE id = %s""",
                    (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        """UPDATE railway.Offers SET
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
                            offer.id,
                        ),
                    )
                    connection.commit()
                    offerj = {
                        "ID": offer.id,
                        "Id_flight": offer.id_flight,
                        "Discount": offer.discount,
                        "Customer_type": offer.customer_type,
                        "Flight_type": offer.flight_type,
                    }
                    return offerj
                else:
                    return {"error": "id de vuelo no encontrado"}
            else:
                return {"error": "tipo de vuelo no encontrado"}
        else:
            return {"error": "reserva no encontrada"}

    def delete_offer(self, id: int):
        connection = pymysql.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        cursor.execute(
            """SELECT * FROM railway.Offers WHERE id = %s""",
            (id,),
        )
        result = cursor.fetchone()
        if result:
            cursor.execute("""DELETE FROM railway.Offers WHERE id = %s""", (id,))
            connection.commit()
            return {"message": "Oferta eliminada exitosamente"}
        else:
            return {"error": "oferta no encontrada"}

    def show_offer(self, id: str):
        connection = pymysql.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        if id == "all":
            cursor.execute("""SELECT * FROM railway.Offers""")
            rows = cursor.fetchall()
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
            return rowsj
        else:
            try:
                cursor.execute(
                    """SELECT * FROM railway.Offers WHERE ID = %s""", (id,)
                )
                rows = cursor.fetchone()
                rowj = {
                    "id": rows[0],
                    "Id_flight": rows[1],
                    "Discount": rows[2],
                    "Customer_type": rows[3],
                    "Flight_type": rows[4],
                }
                return rowj
            except:
                return {"message": "datos no válidos"}