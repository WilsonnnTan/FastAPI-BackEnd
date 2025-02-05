from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.models.user import UserTable
from app.schemas.user import UserinDB, User, Token, TokenData
from app.auth.jwt import create_access_token
from app.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer is used to declare the token URL

# Dependency to get the DB session
def get_db():
    db = SessionLocal()  # Create a session
    try:
        yield db
    finally:
        db.close()  # Close the session when done
        
# Function for matching password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username:str):
    if username in db:
        user_data = db[username]
        return UserinDB(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

    

# def get_password_hash(password: str):
#     return pwd_context.hash(password)

# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()

# @router.post("/register", response_model=User)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):  # Corrected the dependency
#     db_user = get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_password = get_password_hash(user.password)
#     db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # Updated login to use OAuth2PasswordRequestForm
# @router.post("/login", response_model=Token)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  
#     db_user = get_user_by_email(db, form_data.username)
#     if not db_user or not pwd_context.verify(form_data.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": db_user.id})
#     return {"access_token": access_token, "token_type": "bearer"}

