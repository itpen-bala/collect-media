from databases import Database
from sqlalchemy import create_engine, MetaData


DATABASE_URL = "postgresql://media_user:qwerty@127.0.0.1:5432/main_db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL,
)
