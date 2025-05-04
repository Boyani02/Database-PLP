from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SignUpModel(BaseModel):
    id:Optional[int] = None
    username:str
    email:str
    password:str
    is_active:Optional[bool]
    is_staff:Optional[bool]
    


    class Config:
        from_attributes=True
        json_schema_extra={
            'example':{
                "username":"jane",
                "email":"janedoe@gmail.com",
                "password":"1234",
                "is_active":True,
                "is_staff":False
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str='290ac31feacee933ea53d3128c2d0f1691782dffb1bb5f7c8259f0ae052db2b0'     


class LoginModel(BaseModel):
    username:str
    password:str


class TripModel(BaseModel):
    id:Optional[int]
    name:str
    description:str
    start_date:datetime
    end_date:datetime
    trip_status:Optional[str]="PENDING"
    user_id:Optional[int]


class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Summer Safari",
                "description": "A 7-day wildlife adventure in the Maasai Mara.",
                "start_date": "2025-07-01T08:00:00",
                "end_date": "2025-07-07T18:00:00"
            }
        }    
    
class TripStatusModel(BaseModel):
    trip_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                 "trip_status":"PENDING"
            }
        }