#Standard Modules/Libs
from fastapi import APIRouter

#Custom Modules/Libs
from app.api.api_v1.endpoints import address_book


apps = APIRouter()
apps.include_router(address_book.router)