from models.flight_model import *
from typing import Optional

class Firts_flight_model (FlightModel):
    premium_cost : Optional[float]
    class Config:
        from_attributes = True


class fly_firts_UpdateModel (Firts_flight_model ):
    class Config:
        from_attributes = True