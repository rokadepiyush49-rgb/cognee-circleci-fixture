"""25 failing tests, only on the `many-failures` branch.

Used to check that the connector caps how many failing tests it keeps per job.
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("CIRCLE_BRANCH") != "many-failures",
    reason="only runs on the many-failures branch",
)


@pytest.mark.parametrize("n", range(25))
def test_case_fails(n):
    assert n < 0, f"case {n} failed on purpose"
