import os

from dotenv import load_dotenv


load_dotenv()


"""ENV VAR"""
DB_URL = os.getenv("DB_URL")
