from db.session import engine
from db.base import Base
from db import models

def init_db():
    _ = models
    Base.metadata.create_all(bind=engine)
