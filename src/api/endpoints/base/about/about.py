#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run API for Home
"""
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from helpers.limit_helpers import handle_rate_limit

router = APIRouter()


# Note: the route decorator must be above the limit decorator, not below it
@router.get("/about")
@handle_rate_limit("3/minute")
async def about(request: Request):
    """
    About endpoint
    :param request:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "You can read all about us, but only 3 times per minute"},
    )
