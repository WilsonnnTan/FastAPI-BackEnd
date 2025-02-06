from fastapi import APIRouter, Depends, HTTPException, status, Form
from psycopg2 import IntegrityError
from sqlalchemy import or_
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import re

from app.schemas.user import Token, TokenData, User
from app.database import SessionLocal
from app.models.user import UserTable
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer is used to declare the token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Regex pattern for validating usernames
USERNAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$'

# Regex for validating email format
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


# Dependency to get the DB session
def get_db():
    db = SessionLocal()  # Create a session
    try:
        yield db
    finally:
        db.close()  # Close the session when done
        
        
# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to Check Password Strength
def is_password_strong(password: str) -> bool:
    if len(password) < 8:
        return False  # Password must be at least 8 characters long
    if not any(char.isdigit() for char in password):
        return False  # Password must contain at least one digit
    if not any(char.isupper() for char in password):
        return False  # Password must contain at least one uppercase letter
    if not any(char.islower() for char in password):
        return False  # Password must contain at least one lowercase letter
    return True


# Function for Hashing password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to add a new user in Database
def create_user_in_db(db: Session, username: str, email: str, hashed_password: str):
    try:
        # Create a new instance of the UserTable
        new_user = UserTable(username=username, email=email, hashed_password=hashed_password)
        
        # Add the new user to the session
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user

    except IntegrityError as e:
        # Handle unique constraint violations (e.g., username or email already exists)
        db.rollback()  # Rollback the session to undo any changes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists. Please choose another one."
        )
    except Exception as e:
        # Handle any other unforeseen database errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user. Please try again later."
        )


# Retrieves a user from the database by either username or email.
def get_user(db: Session, usernameorEmail:str):
    user = db.query(UserTable).filter(
        or_(
            UserTable.username == usernameorEmail,
            UserTable.email == usernameorEmail
        )
    ).first()
    return user


# Function to authenticate a user by checking their username and password.
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


# Function to create Token for user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to Retrieves the current authenticated user from the token, verifying its validity and decoding the username.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, usernameorEmail=token_data.username)
    if user is None:
        raise credential_exception
    
    return user


# Route for Authenticates the user and generates an access token if the login is successful.
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta= access_token_expires)
    return{"access_token": access_token, "token_type": "bearer"}

# Route for Registration
@router.post("/register")
def register_user(
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
    ):
    # Validate Username Format
    if not re.match(USERNAME_REGEX, username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username. Username must start with a letter and can only contain letters, numbers, and underscores. The length should be between 3 and 20 characters.")
    
    # Validate Email Format
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
    
    # Validate password strength
    if not is_password_strong(password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long and contain a mix of uppercase, lowercase, and digits.")
    
    # Check if email is already taken
    existing_user = get_user(db, email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(password)
    
    try:
        create_user_in_db(db, username=username, email=email, hashed_password=hashed_password)
    except Exception as e:
        # The exception from `create_user_in_db` will be automatically raised with the appropriate detail
        raise e
    
    return {"message": "User registered", "username": username, "email": email}


# Route to retrieve the current authenticated user's information (just for checking the Authorization)
@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


