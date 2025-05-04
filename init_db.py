from database import engine,Base
from models import User,Trip

Base.metadata.create_all(bind=engine)