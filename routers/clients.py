from Classes.standart_client import Standardclient
from Classes.premium_client import PremiumClient
from fastapi import APIRouter, Depends, HTTPException
from controller.bd_controller_clients import DatabaseControllerClient
from models.standart_client_model import *
from models.premium_client_model import *

bd_object_client = DatabaseControllerClient() 

client_router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@client_router.post("/add/standartclient")
async def add_standartclient(standart_client : Standart_clientmodel):
    """
    Add a standart client to database
    """
    return bd_object_client.insert_client(Standardclient(id =0, name=standart_client.name, contact= standart_client.contact,bookings = standart_client.bookings ,email= standart_client.email))

@client_router.post("/add/premiumclient")
async def add_premiumclient(premium_client : Premium_clientmodel):
    """
    Add a premium client to database
    """
    return bd_object_client.insert_client(PremiumClient(id =0, name= premium_client.name, contact= premium_client.contact,bookings = premium_client.bookings ,email= premium_client.email))

@client_router.put("/edit/standartclient")
def edit_client(standart_client : Standart_clientUpdateModel):
    """
    edit a standart client to database
    """ 
    return bd_object_client.edit_client(Standardclient(id = standart_client.id, name=standart_client.name, contact= standart_client.contact,bookings = standart_client.bookings ,email= standart_client.email))

@client_router.put("/edit/premiumclient")
def edit_client(premium_client : Premium_clientmodel):
    """
    edit a standart client to database
    """ 
    return bd_object_client.edit_client(PremiumClient(id = premium_client.id, name=premium_client.name, contact= premium_client.contact,bookings = premium_client.bookings ,email= premium_client.email))

@client_router.delete("/delete/client/{id}/{client_type}")
def delete_client(id:int = 1 , client_type:str = "client type"):
    """
    delete a standartclient to database
    """ 
    return bd_object_client.delete_client(id= id, client_type=client_type)

@client_router.get("/get/clients/{id}/{table_name}")
def show_client(id:str = "all or id", table_name:str = "standart_client or premium_client"):
    """
     show clients
    """ 
    return bd_object_client.show_client(id=id,table_name=table_name)

@client_router.get("/get/premiumclient")
def show_premiumclient():
    """
    show premiums clients
    """ 
    return bd_object_client.premium_clients()