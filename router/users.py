from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError
from models.User import User, UserInDB
from utils.jwt_security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from mongo_db import DATABASE

users_router = APIRouter()
db = DATABASE
collection = db.connect_collection(db_name="minerva-world", collection="users")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@users_router.post("/create")
def register(user: User):
    if collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered"
        )
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    user_to_save = user_in_db.dict()
    user_to_save.pop("password")
    collection.insert_one(user_to_save)
    return {"msg": "User registered successfully"}


@users_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User(**collection.find_one({"username": form_data.username}))
    if not user or not verify_password(form_data.password, get_password_hash(form_data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = User(**collection.find_one({"username": username}))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return JSONResponse(user.dict())
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from e