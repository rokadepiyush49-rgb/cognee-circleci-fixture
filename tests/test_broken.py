"""Tests that fail on purpose, so the connector has failure output to ingest.

They pass on the `green` branch, which gives a fully passing pipeline.
"""

import os

import pytest

from app.calc import add, parse_config

pytestmark = pytest.mark.skipif(
    os.environ.get("CIRCLE_BRANCH") == "green",
    reason="green branch: intentional failures are off",
)


def test_add_wrong_expectation():
    # Plain assertion failure: short, readable message.
    assert add(2, 2) == 5


def test_parse_config_missing_key():
    # Uncaught exception instead of an assertion.
    config = parse_config("retries = 3")
    assert config["timeout"] == "30"


def test_long_failure_message():
    # Message well over 500 chars, to test that the connector truncates it.
    expected = "x" * 400
    actual = "y" * 400
    assert actual == expected, f"payload mismatch: expected {expected!r}, got {actual!r}"
