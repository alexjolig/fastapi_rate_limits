#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from fastapi import status, Request
from fastapi.responses import JSONResponse
from limits.aio.strategies import MovingWindowRateLimiter
from limits.storage import storage_from_string
from limits import parse

from core.config import get_settings


redis = storage_from_string(
    f"async+redis://{get_settings().REDIS_HOST}:{get_settings().REDIS_PORT}"
)

moving_window = MovingWindowRateLimiter(redis)


def handle_rate_limit(limitation_item: str):
    """
    This is used as a decorator for API routers to implement rate limitation
    :param limitation_item: limitation value (e.g: "2/minute", "10/day")
    :return: response
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            email = request.state.user.claims["preferred_username"]
            is_allowed = await moving_window.hit(parse(limitation_item), email)
            if not is_allowed:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"message": "Maximum requests per time exceeded!"},
                )
            return await func(*args, request, **kwargs)

        return wrapper

    return decorator
