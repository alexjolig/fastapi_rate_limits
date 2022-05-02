#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import json

from tests.unit.constants import NOT_AUTHENTICATED_RESPONSE
from api.endpoints.base.home.home import homepage


@pytest.mark.asyncio
def test_homepage_api(get_app):
    response = get_app.get("/")
    assert response.status_code == 401
    assert response.json() == NOT_AUTHENTICATED_RESPONSE


@pytest.mark.asyncio
async def test_homepage(get_request_object):
    response = await homepage.__wrapped__(request=get_request_object)
    assert json.loads(response.body) == {"message": "Hello There!"}
