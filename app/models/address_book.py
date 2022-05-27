#Standard Modules/Libs
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#Custom Modules/Libs
from app.db.base_class import Base


class AddressBook(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    longitude = Column(String(256), nullable = False)
    latitude = Column(String(256), nullable = False)