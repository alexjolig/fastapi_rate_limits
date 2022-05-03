#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test related to redis module
"""
from unittest import mock

import pytest

from redis.redis import coredis
from tests.unit.mocks import Redis


@mock.patch("redis.redis.Redis")
@pytest.mark.asyncio
async def test_handle_rate_limit(get_mocked_storage, get_request_object):

    get_mocked_storage.side_effect = Redis
    await coredis()
