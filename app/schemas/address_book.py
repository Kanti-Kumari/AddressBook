#Standard Modules/Libs
from pydantic import BaseModel, HttpUrl
from typing import Sequence


class AddressBookBase(BaseModel):
    id: int


class AddressBookCreate(AddressBookBase):
    name: str
    longitude: str
    latitude: str

class AddressBookUpdate(AddressBookBase):
    name: str
    longitude: str
    latitude: str

# Properties shared by models stored in DB
class AddressBookInDBBase(AddressBookBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class AddressBook(AddressBookInDBBase):
    id: int

# Properties properties stored in DB
class AddressBookInDB(AddressBookInDBBase):
    pass


class AddressBookSearchResults(BaseModel):
    results: Sequence[AddressBook]