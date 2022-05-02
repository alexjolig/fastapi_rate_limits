#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test related to config module
"""
import pytest

from core.config import Settings


@pytest.mark.parametrize(
    "value, expected, error",
    [
        (
            [
                "http://localhost",
                "http://localhost:4200",
                "http://localhost:3000",
                "http://localhost:8080",
                "http://local.dockertoolbox.tiangolo.com",
            ],
            [
                "http://localhost",
                "http://localhost:4200",
                "http://localhost:3000",
                "http://localhost:8080",
                "http://local.dockertoolbox.tiangolo.com",
            ],
            None,
        ),
        (
            '["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", '
            '"http://local.dockertoolbox.tiangolo.com"]',
            '["http://localhost", "http://localhost:4200", "http://localhost:3000", "http://localhost:8080", '
            '"http://local.dockertoolbox.tiangolo.com"]',
            None,
        ),
        (
            "http://localhost,http://localhost:4200",
            ["http://localhost", "http://localhost:4200"],
            None,
        ),
        ("http://localhost", ["http://localhost"], None),
        ([], [], None),
        ("", [""], None),
        (1, 1, ValueError),
        (None, None, ValueError),
    ],
)
def test_assemble_cors_origin(value, expected, error):
    if error is None:
        assert Settings.assemble_cors_origins(value) == expected
    else:
        with pytest.raises(error):
            Settings.assemble_cors_origins(value)
