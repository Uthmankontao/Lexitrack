from .. import models, schemas, utils
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user:schemas.CreateUser, db: Session= Depends(get_db)):
    db_query = db.query(models.User).filter(models.User.email == user.email).first()
    if db_query:
        raise HTTPException(detail="This user already exist", status_code=status.HTTP_401_UNAUTHORIZED)
    #hash a password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(detail=f"User with {id} doesn't exist", status_code=status.HTTP_404_NOT_FOUND)
    return user 