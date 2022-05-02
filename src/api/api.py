#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
All the API routers from all microservices will be centralised here
"""
from fastapi import APIRouter

from api.endpoints.base import base


api_router = APIRouter()

api_router.include_router(base.api_router)
