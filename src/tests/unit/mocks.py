#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
All the mock-up objects for the tests
"""
from functools import wraps

from limits.aio import storage
from limits.aio.strategies import MovingWindowRateLimiter

memory_storage = storage.MemoryStorage("async+memory")
moving_window = MovingWindowRateLimiter(memory_storage)
