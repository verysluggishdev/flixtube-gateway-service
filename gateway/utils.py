from passlib.context import CryptContext
from datetime import datetime
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_unique_file_name(filename):
    current_time = str(datetime.now())
    unique_file_name = f"{filename}@{current_time}"
    return base64.b64encode(unique_file_name.encode()).decode()