from .base import metadata, engine
from .postgres import image_files

metadata.create_all(bind=engine)
