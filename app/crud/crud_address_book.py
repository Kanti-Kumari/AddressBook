#Custom Modules/Libs
from app.crud.base import CRUDBase
from app.models.address_book import AddressBook
from app.schemas.address_book import AddressBookCreate, AddressBookUpdate


class CRUDAddress(CRUDBase[AddressBook, AddressBookCreate, AddressBookUpdate]):
    ...


address = CRUDAddress(AddressBook)

