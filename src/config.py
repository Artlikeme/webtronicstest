from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


SECRET_JWT = os.environ.get("SECRET_JWT")
SECRET_PASS = os.environ.get("SECRET_PASS")


HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY")
CLEARBIT_KEY = os.environ.get("CLEARBIT_KEY")
