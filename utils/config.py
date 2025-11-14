import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL","http://localhost:8000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME","Admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD","Admin123")
BASIC_TOKEN = os.getenv("BASIC_TOKEN","YWRtaW46QWRtaW4xMjM=")  # admin:Admin123 base64 encoded