from fastapi import Depends, FastAPI, Response, status  
from fastapi.security import HTTPBearer
from starlette.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers.clients import client_router
from routers.supplier import supplier_router
from routers.offers import offers_router
from routers.fligh import flight_router
from routers.booking import bookings_router

app = FastAPI(title="Travel company API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(bookings_router)
app.include_router(offers_router)
app.include_router(flight_router)
app.include_router(supplier_router)


@app.get("/")
async def root():
    return {"Hello": "Travel company API"}





