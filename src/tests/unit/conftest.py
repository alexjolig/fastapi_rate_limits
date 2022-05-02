#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pytest's conftest.py file. Pytest will automatically reads all the fixtures defined in this file
"""
from unittest import mock

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from fastapi_azure_auth.user import User

from main import app
from core.config import Settings
from tests.unit.constants import FAKE_ACCESS_TOKEN


@pytest.fixture(scope="module")
def get_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def get_settings(request):
    with mock.patch("helpers.helpers.get_settings") as mocked_settings:
        mocked_settings.return_value = Settings(
            OPENAPI_CLIENT_ID="OPENAPI_CLIENT_ID",
            APP_CLIENT_ID="APP_CLIENT_ID",
            TENANT_ID="TENANT_ID",
        )
        yield


def get_user():
    return User(
        claims={"name": "Test User", "preferred_username": "test.user@email.com"},
        access_token=FAKE_ACCESS_TOKEN,
        aud="cbf80793-af37-44d7-b65c-05acd44b55e2",
        tid="c0f805f5-0b86-463d-ab5c-565a54d142b2",
        roles=[],
        scp="user_login",
        name="Test User",
    )


@pytest.fixture
def get_request_object() -> Request:
    return Request({"type": "http", "state": {"user": get_user()}})
