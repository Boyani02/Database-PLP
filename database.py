from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

engine=create_engine("mysql+pymysql://trip_user:trip_password@localhost/adventure", echo=True)
    


Base=declarative_base()

Session=sessionmaker()