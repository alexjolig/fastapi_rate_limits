#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import uvicorn
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from redis.redis import coredis
from api.dependencies import azure_scheme
from api.api import api_router
from core.config import get_settings

app = FastAPI(
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": get_settings().OPENAPI_CLIENT_ID,
    },
)

if get_settings().BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def load_config() -> None:
    """
    Load OpenID config on startup.
    By adding on_event('startup') we're able to load the OpenID configuration immediately,
    instead of doing it when the first user authenticates.
    This isn't required, but makes things a bit quicker. When 24 hours has passed,
    the configuration will be considered out of date, and update when a user does a request.
    """
    await azure_scheme.openid_config.load_config()


app.include_router(
    api_router,
    dependencies=[Security(azure_scheme, scopes=["user_login"])],
)

coredis()  # This will run within the docker container


if __name__ == "__main__":
    asyncio.run(coredis())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
