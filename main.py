from fastapi import Depends, FastAPI, Response, status  
from fastapi.security import HTTPBearer
from datetime import date  
from controller.bd_controller_flight import DatabaseControllerFlight
from controller.bd_controller_clients import DatabaseControllerClient
from Classes.first_class import Firtsclass
from Classes.standart_class import Standartclass
from Classes.standart_client import Standardclient
from Classes.premium_client import PremiumClient
from Classes.booking import Booking
from Classes.offers import Offer
from Classes.supplier import Supplier
from controller.db_controller_bookings import DatabaseControllerBokings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.standart_client_model import *
from models.premium_client_model import *
from models.standart_class_model import *
from models.firts_class_model import *
from models.booking_model import * 
from models.supplier_model import *
from models.offers_model import *

app = FastAPI()
bd_object_flights = DatabaseControllerFlight() 
bd_object_client = DatabaseControllerClient() 
bd_object_booking = DatabaseControllerBokings()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Hello": "Travel company API"}

@app.post("/add/firtsclass")
async def add_firtsclass(firts_class : Firts_flight_model):
    """
    Add a firtsclass to database
    """
    return bd_object_flights.insert_flight(Firtsclass(id=0,origin =firts_class.origin, destination=firts_class.destination, date= firts_class.date, 
                                            positions=firts_class.positions, hour=firts_class.hour, id_agency=firts_class.id_agency, premium_cost=firts_class.premium_cost))
@app.post("/add/offers")
async def add_offers(offer:offermodel):
    """
    Add a offer to database
    """
    return bd_object_client.insert_offer(Offer(id=id, id_flight=offer.id_flight, discount=offer.discount, customer_type=offer.customer_type, flight_type=offer.flight_type))

@app.post("/add/supplier")
async def add_supplier(supplier:Suppliermodel):
    """
    Add a offer to database
    """
    return bd_object_flights.insert_supplier(Supplier(id=id, name=supplier.name, contact=supplier.contact,description=supplier.description))
        
@app.post("/add/standartclass")
async def add_standartclass(standart_class : Standart_flight_model):
    """
    Add a standart class to database
    """
    return bd_object_flights.insert_flight(Standartclass(id=0,origin =standart_class.origin, destination=standart_class.destination, date= standart_class.date, 
                                            positions=standart_class.positions, hour=standart_class.hour, id_agency=standart_class.id_agency, standart_cost=standart_class.standart_cost))
    
@app.post("/add/standartclient")
async def add_standartclient(standart_client : Standart_clientmodel):
    """
    Add a standart client to database
    """
    return bd_object_client.insert_client(Standardclient(id =0, name=standart_client.name, contact= standart_client.contact,bookings = standart_client.bookings ,email= standart_client.email))
    
@app.post("/add/premiumclient")
async def add_premiumclient(premium_client : Premium_clientmodel):
    """
    Add a premium client to database
    """
    return bd_object_client.insert_client(PremiumClient(id =0, name= premium_client.name, contact= premium_client.contact,bookings = premium_client.bookings ,email= premium_client.email))

@app.post("/add/booking")
def add_booking(booking : Bookingmodel):
    """
    edit a standart client to database
    """ 
    return bd_object_booking.insert_booking(Booking(id=1, cant_positions=booking.cant_positions, id_flight=booking.id_flight, id_client=booking.id_client,
                                            type_client=booking.type_client, type_flight=booking.type_flight, cost_position=0))

@app.put("/edit/standartclient")
def edit_client(standart_client : Standart_clientUpdateModel):
    """
    edit a standart client to database
    """ 
    return bd_object_client.edit_client(Standardclient(id = standart_client.id, name=standart_client.name, contact= standart_client.contact,bookings = standart_client.bookings ,email= standart_client.email))

@app.put("/edit/booking")
def edit_booking(cant_position:int = 1 , id_booking:int = 1):
    """
    edit a standart client to database
    """ 
    return bd_object_booking.edit_booking(cant_position, id_booking)
@app.put("/edit/supplier")
async def add_supplier(id:int=1,name:str="name", contact:int=0,description:str="description"):
    """
    edit supplier to database
    """
    return bd_object_flights.edit_supplier(Supplier(id=id, name=name, contact=contact,description=description))

@app.put("/edit/premiumclient")
def edit_client(premium_client : Premium_clientmodel):
    """
    edit a standart client to database
    """ 
    return bd_object_client.edit_client(PremiumClient(id = premium_client.id, name=premium_client.name, contact= premium_client.contact,bookings = premium_client.bookings ,email= premium_client.email))

@app.put("/edit/offer")
def edit_offer(offer: offerUpdateModel):
    """
    edit a standart client to database
    """ 
    return bd_object_client.edit_offer(Offer(id= offer.id,id_flight=offer.id_flight, discount=offer.discount, customer_type=offer.customer_type,flight_type=offer.flight_type))

@app.put("/edit/firtsclass")
def edit_flight(firts_class : fly_firts_UpdateModel):
    """
    edit a firtsclass to database
    """ 
    return bd_object_flights.edit_flight(Firtsclass(id= firts_class.id,origin=firts_class.origin, destination= firts_class.destination, date = firts_class.date, positions=firts_class.positions, hour=firts_class.hour, 
                                                       id_agency=firts_class.id_agency, premium_cost=firts_class.premium_cost))


@app.put("/edit/standartclass")
def edit_flight(standart_class : fly_standart_UpdateModel):
    """
    edit a standartclass to database
    """ 
    return bd_object_flights.edit_flight(Standartclass(id= standart_class.id,origin=standart_class.origin, destination= standart_class.destination, date = standart_class.date, positions=standart_class.positions, hour=standart_class.hour, 
                                                       id_agency=standart_class.id_agency, standart_cost=standart_class.standart_cost))

@app.delete("/delete/flight/{id}/{class_type}")
def delete_flight(id:int = 1 , class_type:str = "flght type"):
    """
    delete a standartclass to database
    """ 
    return bd_object_flights.delete_flight(id= id, class_type=class_type)

@app.delete("/delete/client/{id}/{client_type}")
def delete_client(id:int = 1 , client_type:str = "client type"):
    """
    delete a standartclient to database
    """ 
    return bd_object_client.delete_client(id= id, client_type=client_type)

@app.delete("/delete/supplier/{id}")
def delete_supplier(id:int = 1):
    """
    delete a supplier to database
    """ 
    return bd_object_flights.delete_supplier(id= id)

@app.delete("/delete/booking/{id}")
def delete_booking(id:int = 1):
    """
    delete a bookings to database
    """ 
    return bd_object_booking.delete_booking(id= id)

@app.delete("/delete/offer/{id}")
def delete_offer(id:int = 1 ):
    """
    delete a standartclient to database
    """ 
    return bd_object_client.delete_offer(id= id)

@app.get("/get/clients/{id}/{table_name}")
def show_client(id:str = "all or id", table_name:str = "standart_client or premium_client"):
    """
     show clients
    """ 
    return bd_object_client.show_client(id=id,table_name=table_name)

@app.get("/get/flights/{id}/{table_name}")
def show_flight(id:str = "all or id",table_name:str = "standart_class or firts_class"):
    """
    show flights
    """ 
    return bd_object_flights.show_flight(id=id, table_name=table_name)

@app.get("/get/offers/{id}")
def show_offers(id:str = "all or id"):
    """
    show offers
    """ 
    return bd_object_client.show_offer(id=id)

@app.get("/get/supplier/{id}")
def show_supplier(id:str = "all or id"):
    """
    show supplier
    """ 
    return bd_object_flights.show_supplier(id=id)

@app.get("/get/bookings/{id}")
def show_bookings(id:str = "all or id"):
    """
    show bookings
    """ 
    return bd_object_booking.show_booking(id=id)

@app.get("/get/premiumclient")
def show_premiumclient():
    """
    show premiums clients
    """ 
    return bd_object_client.premium_clients()

@app.get("/get/bill")
def show_bill(id_booking:int = 1,payment_method:str = "payment_method"):
    """
    show bill
    """ 
    return bd_object_booking.show_bill(id_booking=id_booking,payment_method=payment_method)


