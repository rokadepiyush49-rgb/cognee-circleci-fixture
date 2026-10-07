def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def parse_config(raw):
    key, _, value = raw.partition("=")
    return {key.strip(): value.strip()}
