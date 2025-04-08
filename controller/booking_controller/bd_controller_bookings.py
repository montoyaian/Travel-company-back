from Classes.bill import Bill
from Classes.booking import Booking
import pymysql
from database.config import DATABASE_CONFIG
from fastapi import HTTPException
from utils.standard_response import standard_response


class DatabaseControllerBookings:
    """
    This class is used to manage bookings in the database.
    """

    def insert_booking(self, booking: Booking):
        try:
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor()

            flightType = "standart_class" if booking.type_flight == "standart_class" else "first_class"
        
            cursor.execute(f"""SELECT * FROM railway.{flightType} WHERE ID= %s""", (booking.id_flight,))
        

            flight = cursor.fetchone()
            if not flight or flight[4] < booking.cant_positions:
                raise HTTPException(status_code=400, detail="Vuelo no disponible o asientos insuficientes")

            if booking.type_client == "standart_client":
                cursor.execute("""SELECT * FROM railway.standart_client WHERE ID= %s""", (booking.id_client,))
            elif booking.type_client == "premium_client":
                cursor.execute("""SELECT * FROM railway.premium_client WHERE ID= %s""", (booking.id_client,))
            else:
                raise HTTPException(status_code=400, detail="Tipo de cliente no válido")

            client = cursor.fetchone()
            if not client:
                raise HTTPException(status_code=404, detail="Cliente no encontrado")

          
            cursor.execute("""SELECT * FROM railway.offers WHERE Id_flight= %s AND Customer_type = %s""",
                           (booking.id_flight, booking.type_client))
            offer = cursor.fetchone()
            discount = float(offer[2]) if offer else 0.0

            price_position = flight[7]
            new_cost_position = price_position - (price_position * discount / 100)

            # Actualizar posiciones del vuelo
            flight_new_positions = flight[4] - booking.cant_positions
            if booking.type_flight == "standart_class":
                cursor.execute("""UPDATE railway.standart_class SET Positions=%s WHERE id = %s""",
                               (flight_new_positions, flight[0]))
            else:
                cursor.execute("""UPDATE railway.first_class SET Positions=%s WHERE id = %s""",
                               (flight_new_positions, flight[0]))
            connection.commit()

            client_new_bookings = client[3] + 1
            if booking.type_client == "standart_client":
                cursor.execute("""UPDATE railway.standart_client SET Bookings=%s WHERE id = %s""",
                               (client_new_bookings, client[0]))
            else:
                cursor.execute("""UPDATE railway.premium_client SET Bookings=%s WHERE id = %s""",
                               (client_new_bookings, client[0]))
            connection.commit()

            cursor.execute("""INSERT INTO railway.bookings(
                Cant_positions,
                Id_flight,
                Id_client,
                Type_flight,
                Type_client,
                Cost_position
            ) VALUES (%s, %s, %s, %s, %s, %s)""",
                           (booking.cant_positions, booking.id_flight, booking.id_client,
                            booking.type_flight, booking.type_client, new_cost_position))
            connection.commit()

            bookingj = {
                "cant_position": booking.cant_positions,
                "Id_flight": booking.id_flight,
                "Id_client": booking.id_client,
                "Type_flight": booking.type_flight,
                "Type_client": booking.type_client,
                "Cost_position": new_cost_position,
            }
            if discount > 0:
                bookingj["offer"] = offer[0]
                bookingj["discount"] = discount

            return standard_response("Reserva insertada exitosamente", bookingj, 201)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al insertar reserva: {str(e)}")

    def delete_booking(self, id: int):
        try:
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor()

            cursor.execute("""SELECT * FROM railway.bookings WHERE ID= %s""", (id,))
            booking = cursor.fetchone()
            if not booking:
                raise HTTPException(status_code=404, detail="Reserva no encontrada")

            if booking[4] == "standart_class":
                cursor.execute("""SELECT * FROM railway.standart_class WHERE ID= %s""", (booking[2],))
            else:
                cursor.execute("""SELECT * FROM railway.first_class WHERE ID= %s""", (booking[2],))
            flight = cursor.fetchone()
            flight_new_positions = flight[4] + booking[1]
            if booking[4] == "standart_class":
                cursor.execute("""UPDATE railway.standart_class SET Positions=%s WHERE id = %s""",
                               (flight_new_positions, flight[0]))
            else:
                cursor.execute("""UPDATE railway.first_class SET Positions=%s WHERE id = %s""",
                               (flight_new_positions, flight[0]))
            connection.commit()

            if booking[5] == "standart_client":
                cursor.execute("""SELECT * FROM railway.standart_client WHERE ID= %s""", (booking[3],))
            else:
                cursor.execute("""SELECT * FROM railway.premium_client WHERE ID= %s""", (booking[3],))
            client = cursor.fetchone()
            client_new_bookings = client[3] - 1
            if booking[5] == "standart_client":
                cursor.execute("""UPDATE railway.standart_client SET Bookings=%s WHERE id = %s""",
                               (client_new_bookings, client[0]))
            else:
                cursor.execute("""UPDATE railway.premium_client SET Bookings=%s WHERE id = %s""",
                               (client_new_bookings, client[0]))
            connection.commit()

            cursor.execute("""DELETE FROM railway.bookings WHERE ID= %s""", (id,))
            connection.commit()

            return standard_response("Reserva eliminada exitosamente", None, 200)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar reserva: {str(e)}")

    def show_booking(self, id: str):
        try:
            connection = pymysql.connect(**DATABASE_CONFIG)
            cursor = connection.cursor()

            if id == "all":
                cursor.execute("""SELECT * FROM railway.bookings""")
                rows = cursor.fetchall()
                rowsj = [
                    {
                        "id": i[0],
                        "Cant_position": i[1],
                        "Id_flight": i[2],
                        "Id_client": i[3],
                        "Type_flight": i[4],
                        "Type_client": i[5],
                        "Cost_position": i[6],
                    }
                    for i in rows
                ]
                return standard_response("Listado de reservas", rowsj, 200)
            else:
                cursor.execute("""SELECT * FROM railway.bookings WHERE id = %s""", (id,))
                booking = cursor.fetchone()
                if not booking:
                    raise HTTPException(status_code=404, detail="Reserva no encontrada")

                bookingj = {
                    "id": booking[0],
                    "Cant_position": booking[1],
                    "Id_flight": booking[2],
                    "Id_client": booking[3],
                    "Type_flight": booking[4],
                    "Type_client": booking[5],
                    "Cost_position": booking[6],
                }
                return standard_response("Reserva encontrada", bookingj, 200)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener reservas: {str(e)}")