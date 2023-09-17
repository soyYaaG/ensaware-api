import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from authorization.v1.router import router as authorization
from profile.v1.router import router as profile

from utils.exception.ensaware import EnsawareException, EnsawareExceptionBase, EnsawareExceptionHandler
from utils.settings import Settings


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


settings = Settings()
ensaware_exception_handler = EnsawareExceptionHandler()


app = FastAPI(
    title='Ensaware',
    version='0.0.1',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    responses={
        400: {
            'model': EnsawareExceptionBase
        },
        401: {
            'model': EnsawareExceptionBase
        }
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=tuple(settings.cors_origins.split(',')),
    allow_credentials=True,
    allow_methods=tuple(settings.cors_methods.split(',')),
    allow_headers=["*"],
)
app.exception_handler(EnsawareException)(ensaware_exception_handler.ensaware)

add_pagination(app)


app.include_router(
    authorization,
    prefix='/v1/authorization',
    tags=['v1 - authorization']
)


app.include_router(
    profile,
    prefix='/v1/profile',
    tags=['v1 - profile']
)