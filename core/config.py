import os

from dotenv import load_dotenv


load_dotenv()


"""ENV VAR"""
DB_URL = os.getenv("DB_URL")

JWT_KEY = os.getenv("JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM")

SUPERUSER_USERNAME = os.getenv("SUPERUSER_USERNAME")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")
