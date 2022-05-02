#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Here lies the project configurations
"""
import os
from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, validator


class AzureActiveDirectory(BaseSettings):
    """
    Data from Azure AD (e.g Tenant, registered apps,...)
    """

    OPENAPI_CLIENT_ID: str = Field(default="", env="OPENAPI_CLIENT_ID")
    APP_CLIENT_ID: str = Field(default="", env="APP_CLIENT_ID")
    TENANT_ID: str = Field(default="", env="TENANT_ID")


class Settings(AzureActiveDirectory):
    """
    All the settings for the app
    """

    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:8000"]
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """
        Validate cors list
        """
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)


@lru_cache()
def get_settings():
    """
    Cached methods to create an instance of Setting
    :return: An instance of Setting class
    """
    return Settings()
