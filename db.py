import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()
DB_CREDENTIALS = os.getenv("DB_CREDENTIALS")
engine = sqlalchemy.create_engine(f"postgresql://{DB_CREDENTIALS}@localhost/addy")
