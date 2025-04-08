from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

path = os.getenv("POSTGRE_DATABASE_URL")

Base = declarative_base()