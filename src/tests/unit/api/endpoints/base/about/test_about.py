#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import pytest

from api.endpoints.base.about.about import about
from tests.unit.constants import NOT_AUTHENTICATED_RESPONSE


@pytest.mark.asyncio
def test_about_api(get_app):
    response = get_app.get("/about")
    assert response.status_code == 401
    assert response.json() == NOT_AUTHENTICATED_RESPONSE


@pytest.mark.asyncio
async def test_about(get_request_object):
    response = await about.__wrapped__(get_request_object)
    assert json.loads(response.body) == {
        "message": "You can read all about us, but only 3 times per minute"
    }
