import pytest

from app.calc import add, divide, parse_config


def test_add():
    assert add(2, 3) == 5


def test_divide():
    assert divide(9, 3) == 3


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_parse_config():
    assert parse_config("retries = 3") == {"retries": "3"}
