import os

from io import StringIO
import pytest
import yaml

from envsub import sub


@pytest.fixture()
def envvars(params, monkeypatch):
    if "envvars" in params:
        for key, val in params["envvars"].items():
            monkeypatch.setenv(key, val)
    yield params.get("envvars")


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "envvars": {"name": "Bob", "alt": "Harriet"},
                "stdin": [
                    "str1: Hello, ${name}!",
                    "str2: Hello, also ${alt}!",
                ],
                "expected": {
                    "str1": "Hello, Bob!",
                    "str2": "Hello, also Harriet!",
                },
            },
            id="All vars",
        ),
        pytest.param(
            {
                "envvars": {"name": "Bob"},
                "stdin": [
                    "str1: Hello, ${name}!",
                    "str2: Hello, also ${alt}!",
                ],
                "expected": {
                    "str1": "Hello, Bob!",
                    "str2": "Hello, also ${alt}!",
                },
            },
            id="Missing vars stays unset",
        ),
        pytest.param(
            {
                "envvars": {"name": "Bob"},
                "stdin": [
                    "str1: Hello, ${name}!",
                    "str2: Hello, also ${alt-Harriet}!",
                ],
                "expected": {
                    "str1": "Hello, Bob!",
                    "str2": "Hello, also Harriet!",
                },
            },
            id="Missing vars with default",
        ),
    ],
)
def test_sub(envvars, params):
    downstream = StringIO("\n".join(params["stdin"]))
    with sub(downstream) as upstream:
        res = yaml.safe_load(upstream)

    assert res == params["expected"]
