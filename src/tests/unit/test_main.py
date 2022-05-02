#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test related to main module
"""
from unittest import mock
import pytest

from main import load_config


@mock.patch("main.azure_scheme.openid_config.load_config")
@pytest.mark.asyncio
async def test_load_config(mock_load_config):
    await load_config()
