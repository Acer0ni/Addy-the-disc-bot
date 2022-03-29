import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_CREDENTIALS = os.getenv("DB_CREDENTIALS")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
engine = sqlalchemy.create_engine(f"postgresql://{DB_CREDENTIALS}@{DB_HOSTNAME}/addy")
Session = sessionmaker(engine)
