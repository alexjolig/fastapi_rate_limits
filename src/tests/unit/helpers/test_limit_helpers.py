#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test related to helpers module
"""
import time
from unittest import mock

import pytest

from tests.unit.constants import SUCCESS_RESPONSE
from tests.unit.mocks import moving_window
from helpers.limit_helpers import handle_rate_limit


@mock.patch("helpers.limit_helpers.moving_window.hit")
@pytest.mark.asyncio
async def test_handle_rate_limit(get_mocked_storage, get_request_object):
    @handle_rate_limit("3/minute")
    async def three_per_minute(*args, **kwargs):
        return SUCCESS_RESPONSE

    @handle_rate_limit("2/second")
    async def two_per_second(*args, **kwargs):
        return SUCCESS_RESPONSE

    get_mocked_storage.side_effect = moving_window.hit
    assert await three_per_minute(request=get_request_object) == SUCCESS_RESPONSE
    assert await three_per_minute(request=get_request_object) == SUCCESS_RESPONSE
    assert await three_per_minute(request=get_request_object) == SUCCESS_RESPONSE
    response = await three_per_minute(request=get_request_object)
    assert response.status_code == 429

    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    response = await two_per_second(request=get_request_object)
    assert response.status_code == 429
    time.sleep(1)
    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    time.sleep(1)
    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    assert await two_per_second(request=get_request_object) == SUCCESS_RESPONSE
    response = await two_per_second(request=get_request_object)
    assert response.status_code == 429
