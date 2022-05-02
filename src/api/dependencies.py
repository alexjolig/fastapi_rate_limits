#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dependencies for all the endpoints
"""
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from core.config import get_settings

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=get_settings().APP_CLIENT_ID,
    scopes={
        f"api://{get_settings().APP_CLIENT_ID}/user_login": "**No client secret needed, leave blank**",
    },
    tenant_id=get_settings().TENANT_ID,
)
