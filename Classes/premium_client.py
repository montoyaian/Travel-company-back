from Classes.client import Client

class PremiumClient(Client):
    def __init__(self, id:int, name:str, contact:int,bookings:int,email:str):
        super().__init__(id, name, contact,bookings,email)
             
    def __str__(self):
        return {"id": self.id,
                "name": self.name,
                "contact": self.contact,
                "bookings": self.bookings,
                "email": self.email,
                }
