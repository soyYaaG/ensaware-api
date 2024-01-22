import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from authorization.v1.router import router as authorization
from career.v1.router import router as career
from domain.v1.router import router as domain
from permission.v1.router import router as permission
from profiles.v1.router import router as profile
from qr.v1.router import router as qr
from user.v1.router import router as user

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
        },
        403: {
            'model': EnsawareExceptionBase
        },
        500: {
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
    career,
    prefix='/v1/career',
    tags=['v1 - career']
)

app.include_router(
    domain,
    prefix='/v1/domain',
    tags=['v1 - domain']
)

app.include_router(
    permission,
    prefix='/v1/permission',
    tags=['v1 - permission']
)

app.include_router(
    profile,
    prefix='/v1/profile',
    tags=['v1 - profile']
)

app.include_router(
    qr,
    prefix='/v1/qr',
    tags=['v1 - qr']
)

app.include_router(
    user,
    prefix='/v1/user',
    tags=['v1 - user']
)
