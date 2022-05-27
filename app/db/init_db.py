#Standard Modules/Libs
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#Custom Modules/Libs
from app import crud, schemas
from app.db import base  
from app.core.config import settings
from app.db.base_class import Base

logger = logging.getLogger(__name__)

ADDRESSES = [
    {
        "id": 1,
        "name": "John Smith",
        "address": [{
            "longitude": "45.2655",
            "latitude": "23.2655"
        }]
        
    },
    {
        "id": 2,
        "name": "Mark",
        "address": [{
            "longitude": "35.2655",
            "latitude": "13.2655"
        }]
        
    },
    {
        "id": 3,
        "name": "Monika",
        "address": [{
            "longitude": "65.2655",
            "latitude": "43.2655", 
        }]
        
    },
]

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly

def init_db(db: Session) -> None:
    # Creating the Tables
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},)

    Base.metadata.create_all(bind=engine)
    for address in ADDRESSES:
        address_in = schemas.AddressBookCreate(
            name=address["name"],
            longitude=address["address"][0].get('longitude'),
            latitude=address["address"][0].get('latitude'),
            )
        crud.crud_address_book.address.create(db, obj_in=address_in)