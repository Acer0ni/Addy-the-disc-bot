import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_CREDENTIALS = os.getenv("DB_CREDENTIALS")
engine = sqlalchemy.create_engine(f"postgresql://{DB_CREDENTIALS}@localhost/addy")
Session = sessionmaker(engine)
