#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Api router for all base service related APIs
"""
from fastapi import APIRouter

from api.endpoints.base.home import home
from api.endpoints.base.about import about

api_router = APIRouter(
    tags=["Base"],
)
api_router.include_router(home.router)
api_router.include_router(about.router)
