from fastapi import APIRouter,status,Depends
from fastapi_jwt_auth import AuthJWT
from models import User,Trip
from schemas import TripModel,TripStatusModel
from fastapi.exceptions import HTTPException
from database import Session,engine
from fastapi.encoders import jsonable_encoder

trip_router=APIRouter(
     prefix='/trips',
     tags=['trips']
)

session=Session(bind=engine)

@trip_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
    
    return {"message":"Hello World"}


@trip_router.post('/trip',status_code=status.HTTP_201_CREATED)
async def plan_a_trip(trip:TripModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
          )
    
    current_user=Authorize.get_jwt_subject()
    
    user=session.query(User).filter(User.username==current_user).first()


    new_trip=Trip(
        name=trip.name,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date
     )
    
    new_trip.user=user

    session.add(new_trip)

    session.commit()

    response={
        "name":new_trip.name,
        "description":new_trip.description,
        "start_date":new_trip.start_date,
        "end_date":new_trip.end_date,
        "id":new_trip.id,
        "trip_status":new_trip.trip_status
    }

    return jsonable_encoder(response)


@trip_router.get('/trips')
async def list_all_trips(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


    if user.is_staff:
        trips = session.query(Trip).all()
        return jsonable_encoder(trips)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not a superuser"
    )

@trip_router.get('/trips/{id}')
async def get_trip_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        trip=session.query(Trip).filter(Trip.id==id).first()

        return jsonable_encoder(trip)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to perform request"
     )

@trip_router.get('/user/trips')
async def get_user_trips(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
          ) 
    
    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.trips)


@trip_router.get('/user/trip/{id}')
async def get_specific_user_trip(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    for trip in user.trips:
        if trip.id == id:
            return jsonable_encoder(trip)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No trip found with this ID for the current user"
    )




@trip_router.put('/trip/update/{id}')
async def update_trip(id:int,trip:TripModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
          )
    
    trip_to_update=session.query(Trip).filter(Trip.id).first()

    trip_to_update.name=trip.name
    trip_to_update.description=trip.description
    trip_to_update.start_date=trip.start_date
    trip_to_update.end_date=trip.end_date

    session.commit()

    response={
            "id":trip_to_update.id,
            "name":trip_to_update.name,
             "description":trip_to_update.description,
             "start_date":trip_to_update.start_date,
             "end_date":trip_to_update.end_date,
             "trip_status":trip_to_update.trip_status
        }

    return jsonable_encoder(trip_to_update)


@trip_router.patch('/trip/update/{id}')
async def update_trip_status(id: int, trip: TripStatusModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    username = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == username).first()

    if current_user.is_staff:
        trip_to_update = session.query(Trip).filter(Trip.id == id).first()


        trip_to_update.trip_status = trip.trip_status

        session.commit()

        response={
            "id":trip_to_update.id,
            "name":trip_to_update.name,
             "description":trip_to_update.description,
             "start_date":trip_to_update.start_date,
             "end_date":trip_to_update.end_date,
             "trip_status":trip_to_update.trip_status
        }

        return jsonable_encoder(trip_to_update)

@trip_router.delete('/trip/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)    
async def delete_a_trip(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    trip_to_delete=session.query(Trip).filter(Trip.id==id).first()

    session.delete(trip_to_delete)

    session.commit()

    return trip_to_delete
    