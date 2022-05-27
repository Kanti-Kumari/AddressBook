#Standard Modules/Libs
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

#Custom Modules/Libs
from app.db.base_class import Base

#Different Schemas for Database Operations
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	def __init__(self, model: Type[ModelType]):
		'''
	        @function : __init__
	        @brief : CRUD object with default methods to Create, Read, Update, Delete (CRUD) and Search
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [] : Returns the model
    	'''
		
		self.model = model

	def get_address(self, db: Session, id:Any) -> Optional[ModelType]:
		'''
	        @function : get_address
	        @brief : Query on matching id
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [dict] : Returns the Address with matching ID
    	'''
		db_data = db.query(self.model).get(id)

		address = {
			"id": db_data.id,
			"name": db_data.name,
			"address": [{
				"longitude": float(db_data.longitude),
				"latitude": float(db_data.latitude)
			}]
			
			}

		return address

	def get_all_addresses(self, db: Session) -> Optional[ModelType]:
		'''
	        @function : get_all_addresses
	        @brief : Query the complete AddressBook
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [list] : Returns the AddressBook List
    	'''

		addressList = []
		addresses = db.query(self.model)

		for item in addresses:
			address = {
				"id": item.id,
				"name": item.name,
				"address": [{
					"longitude": float(item.longitude),
					"latitude": float(item.latitude)
				}]
				
				}

			addressList.append(address)

		return addressList

	def search_addresses(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
		'''
	        @function : search_addresses
	        @brief : Query the max limit AddressBook
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [list] : Returns the AddressBook List with maxm limit
    	'''
		addresses = db.query(self.model).offset(skip).limit(limit).all()

		return addresses

	def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
		'''
	        @function : create
	        @brief : Creates new Address in the AddressBook
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [dict] : Returns the created AddressBook
    	'''

		obj_in_data = jsonable_encoder(obj_in)
		db_obj = self.model(**obj_in_data)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj

	def add_address(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
		'''
	        @function : add_address
	        @brief : Creates and add new Address in the AddressBook
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [dict] : Returns the added AddressBook
    	'''
		obj_in_data = jsonable_encoder(obj_in)

		#Generating unique ID by datatime
		address_id = datetime.now().strftime('%Y%m%d%H%M%S')
		obj_in_data['id'] = int(address_id)		
		db_obj = self.model(**obj_in_data)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)

		address = {
				"id": db_obj.id,
				"name": db_obj.name,
				"address": [{
					"longitude": float(db_obj.longitude),
					"latitude": float(db_obj.latitude)
				}]
				
				}
		return address

	def delete_address(self, db: Session, *, id: int) -> ModelType:
		'''
	        @function : delete_address
	        @brief : Delete an Address from the AddressBook with ID
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [dict] : Returns the deleted AddressBook
    	'''
		try:
			db_obj = db.query(self.model).get(id)
			db.delete(db_obj)
			db.commit()

			address = {
					"id": db_obj.id,
					"name": db_obj.name,
					"address": [{
						"longitude": float(db_obj.longitude),
						"latitude": float(db_obj.latitude)
					}]
					
					}

			return address

		except Exception as e:
			print("%s" % (e))

	def update_address(self, db: Session, *, db_obj: ModelType,
		obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
		'''
	        @function : update_address
	        @brief : Updates Address in the AddressBook
	        @param [model, schema] : A SQLAlchemy model class, A Pydantic model (schema) class
	        @return [dict] : Returns the updated AddressBook
    	'''

    	#TODO Modify the query
		obj_data = jsonable_encoder(db_obj)
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		for field in obj_data:
			if field in update_data:
				setattr(db_obj, field, update_data[field])

		db.add(db_obj)
		db.flush()
		db.commit()
		db.refresh(db_obj)
		return db_obj

	