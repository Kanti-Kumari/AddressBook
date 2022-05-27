#Standard Modules/Libs
from pathlib import Path
from fastapi import FastAPI, APIRouter, Request, Depends
from sqlalchemy.orm import Session

#Custom Modules/Libs
from app import crud
from app.api import deps
from app.api.api_v1.api import apps
from app.core.config import settings


BASE_PATH = Path(__file__).resolve().parent

root_router = APIRouter()
app = FastAPI(title = "Address Book API")

@root_router.get("/")
def root(
    request: Request,
    db: Session = Depends(deps.get_db),) -> dict:
    '''
    Root GET
    '''
    address = crud.crud_address_book.address.get_all_addresses(db=db)
    return {"status": 200, "response": address}


app.include_router(apps, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
