#Standard Modules/Libs
from typing import Generator

#Custom Modules/Libs
from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()