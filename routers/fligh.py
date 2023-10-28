from Classes.first_class import Firtsclass
from Classes.standart_class import Standartclass
from controller.bd_controller_flight import DatabaseControllerFlight
from fastapi import APIRouter, Depends, HTTPException
from models.standart_class_model import *
from models.firts_class_model import *

bd_object_flights = DatabaseControllerFlight() 

flight_router = APIRouter(
    prefix="/flight",
    tags=["Flight"],
)

@flight_router.post("/add/firtsclass")
async def add_firtsclass(firts_class : Firts_flight_model):
    """
    Add a firtsclass to database
    """
    return bd_object_flights.insert_flight(Firtsclass(id=0,origin =firts_class.origin, destination=firts_class.destination, date= firts_class.date, 
                                            positions=firts_class.positions, hour=firts_class.hour, id_agency=firts_class.id_agency, premium_cost=firts_class.premium_cost))

@flight_router.post("/add/standartclass")
async def add_standartclass(standart_class : Standart_flight_model):
    """
    Add a standart class to database
    """
    return bd_object_flights.insert_flight(Standartclass(id=0,origin =standart_class.origin, destination=standart_class.destination, date= standart_class.date, 
                                            positions=standart_class.positions, hour=standart_class.hour, id_agency=standart_class.id_agency, standart_cost=standart_class.standart_cost))

@flight_router.put("/edit/firtsclass/{flight_id}")
def edit_flight(flight_id,firts_class : fly_firts_UpdateModel):
    """
    edit a firtsclass to database
    """ 
    return bd_object_flights.edit_flight(Firtsclass(id= flight_id,origin=firts_class.origin, destination= firts_class.destination, date = firts_class.date, positions=firts_class.positions, hour=firts_class.hour, 
                                                       id_agency=firts_class.id_agency, premium_cost=firts_class.premium_cost))


@flight_router.put("/edit/standartclass/{flight_id}")
def edit_flight(flight_id, standart_class : fly_standart_UpdateModel):
    """
    edit a standartclass to database
    """ 
    return bd_object_flights.edit_flight(Standartclass(id= flight_id,origin=standart_class.origin, destination= standart_class.destination, date = standart_class.date, positions=standart_class.positions, hour=standart_class.hour, 
                                                       id_agency=standart_class.id_agency, standart_cost=standart_class.standart_cost))

@flight_router.delete("/delete/flight/{id}/{class_type}")
def delete_flight(id:int = 1 , class_type:str = "flght type"):
    """
    delete a standartclass to database
    """ 
    return bd_object_flights.delete_flight(id= id, class_type=class_type)

@flight_router.get("/get/flights/{id}/{table_name}")
def show_flight(id:str = "all or id",table_name:str = "standart_class or firts_class"):
    """
    show flights
    """ 
    return bd_object_flights.show_flight(id=id, table_name=table_name)