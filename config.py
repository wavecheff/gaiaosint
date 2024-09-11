import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY_IPSTACK = os.getenv('API_KEY_IPSTACK')
    IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
