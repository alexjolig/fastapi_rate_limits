#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from coredis import Redis


async def coredis():
    """
    Creates a connection to a redis server
    :return:
    """
    client = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        db=0,
    )
    await client.flushdb()
