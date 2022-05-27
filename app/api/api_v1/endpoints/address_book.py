#Standard Modules/Libs
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Any, Optional

#Custom Modules/Libs
from app import crud
from app.api import deps
from app.schemas.address_book import AddressBook, AddressBookCreate, AddressBookSearchResults, AddressBookUpdate

router = APIRouter()

@router.get("/", status_code=200)
def GetAddressesBook(request: Request, db: Session = Depends(deps.get_db),) -> Any:
    '''
        @function : GetAddressBook
        @brief : Route and results the complete AddressBook
        @param [request: Request, db: DB Session Object] : request, db
        @return [dict] : Returns the status code and the AddressBook Dictionary 
    '''
    resultSet = crud.crud_address_book.address.get_all_addresses(db=db)

    if not resultSet:
        # the exception is raised, if empty resultSet
        raise HTTPException(
            status_code=404, detail=f"AddressBook not found"
        )

    return {"status": 200, "response": resultSet}

@router.get("/{address_id}", status_code=200)
def GetAddress(request: Request, address_id: int, db: Session = Depends(deps.get_db), ) -> Any:
    '''
        @function : GetAddress
        @brief : Route and results the AddressBook with matching Address ID
        @param [request: Request, int, db: DB Session Object] : request, address_id, db
        @return [dict] : Returns the status code and the AddressBook Dictionary having this address_id
    '''
    resultSet = crud.crud_address_book.address.get_address(db=db, id=address_id)

    if not resultSet:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"AddressBook with ID {address_id} not found"
        )

    return {"status": 200, "response": resultSet}

@router.post("/", status_code=200)
def AddAddress(*, address_in: AddressBookCreate, db: Session = Depends(deps.get_db)
) -> dict:
    '''
        @function : AddAddress
        @brief : Route and results the complete Newly Added Address Data
        @param [request: Request, schema, db: DB Session Object] : request, AddressBookCreate ,db
        @return [dict] : Returns the status code and the newly added Address Data Dictionary
    '''
    resultSet = crud.crud_address_book.address.add_address(db=db, obj_in=address_in)
    if not resultSet:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"New Data Could not be added"
        )

    return {"status": 200, "response": resultSet}


@router.put("/", status_code=200)
def UpdateAddress(*, db: Session = Depends(deps.get_db),address_in: AddressBookUpdate, ) -> dict:
    '''
        @function : UpdateAddress
        @brief : Route and results the updated AddressBook
        @param [request: Request, db: DB Session Object] : request, db
        @return [dict] : Returns the status code and the Updated AddressBook Data Dictionary 
    '''

    #TODO Verify the Results
    resultSet = crud.crud_address_book.address.update_address(db=db, db_obj=AddressBookCreate, obj_in=address_in)
    
    return {"status": 200, "response": resultSet}


@router.delete("/{address_id}", status_code=200)
def DeleteAddress(*, address_id: int, db: Session = Depends(deps.get_db), ) -> Any:
    '''
        @function : DeleteAddress
        @brief : Route and results the Deleted AddressBook Data
        @param [request: Request, db: DB Session Object] : request, db
        @return [dict] : Returns the status code and the Deleted AddressBook Data Dictionary 
    '''
    resultSet = crud.crud_address_book.address.delete_address(db=db, id=address_id)

    if not resultSet:
        raise HTTPException(
            status_code=404, detail=f"Address can't be updated as it doesn't Exist.. "
        )

    return {"status": 200, "response": resultSet}

@router.get("/search/", status_code=200)
def SearchAddress(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example='keyword'),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    '''
        @function : SearchAddress
        @brief : Route and results the Resultant AddressBook with Keywords
        @param [request: Request, db: DB Session Object] : request, db
        @return [dict] : Returns the status code and the Resultant AddressBook Data Dictionary List 
    '''
    address = crud.crud_address_book.address.search_addresses(db=db, limit=max_results)
    if not keyword:
        return {"results": address}

    results = filter(lambda address: keyword in address.name, address)
    return {"results": list(results)[:max_results]}