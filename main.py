from fastapi import FastAPI
from auth_routes import auth_router
from trip_routes import trip_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app=FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(trip_router)

