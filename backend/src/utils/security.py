# backend/src/utils/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone # <--- Critical: Import timezone directly
from jose import jwt
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

# --- CONFIGURATION ---
SECRET_KEY = os.getenv("SECRET_KEY", "5a702137efeaa8f1276769901cb4e8432b1063da6741da941de95883f6c190b3")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- PASSWORD HASHING ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    # Bcrypt only supports 72 bytes. We truncate to prevent ValueErrors.
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Truncate to 72 bytes to stay within bcrypt's limits
    if isinstance(password, str):
        password = password.encode('utf-8')[:72]
    return pwd_context.hash(password)

# --- JWT TOKEN ---
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # FIX IS HERE: Use 'timezone.utc' directly. 
    # Do NOT write 'datetime.timezone.utc' because 'datetime' refers to the class here.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- GOOGLE OAUTH ---
config = Config('.env') 
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)