import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_CREDENTIALS = os.getenv("DB_CREDENTIALS")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_NAME = os.getenv("DB_NAME")
engine = sqlalchemy.create_engine(f"postgresql://{DB_CREDENTIALS}@{DB_HOSTNAME}/{DB_NAME}")
Session = sessionmaker(engine)
