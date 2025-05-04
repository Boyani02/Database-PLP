from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(50),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    is_active=Column(Boolean,default=False)
    is_staff=Column(Boolean,default=False)
    trips=relationship('Trip', back_populates='user')


    def __repr__(self):
        return f"<User {self.username}>"
    
class Trip(Base):
    TRIP_STATUSES=(
        ('PENDING', 'pending'),
        ('IN PROGRESS', 'in progress'),
        ('COMPLETED', 'completed')
    )


    __tablename__ = 'trips'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    trip_status = Column(ChoiceType(choices=TRIP_STATUSES), default="PENDING")
    user_id = Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='trips')
    
    
    
    def __repr__(self):
        return f"<Trip {self.id}>"
