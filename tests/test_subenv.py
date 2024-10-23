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
        pytest.param(
            {
                "envvars": {
                    "b": "b" * 1000,
                    "e": "e" * 1000,
                },
                "stdin": [
                    f"str1: {'a' * 1000}",
                    "str2: ${b}",
                    f"str3: {'c' * 1000}",
                    f"str4: {'d' * 1000}",
                    "str5: ${e}",
                ],
                "expected": {
                    "str1": "a" * 1000,
                    "str2": "b" * 1000,
                    "str3": "c" * 1000,
                    "str4": "d" * 1000,
                    "str5": "e" * 1000,
                },
            },
            id="More than 4096 chars (yaml buffer size)",
        ),
    ],
)
def test_sub(envvars, params):
    downstream = StringIO("\n".join(params["stdin"]))
    with sub(downstream) as upstream:
        res = yaml.safe_load(upstream)

    assert res == params["expected"]


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "envvars": {"name": "Bob", "alt": "Harriet"},
                "stdin": [
                    "Hello, ${name}!",
                    "Hello, also ${alt}!",
                ],
                "expected": [
                    "Hello, Bob!\n",
                    "Hello, also Harriet!",
                ],
            },
            id="line by line",
        ),
    ],
)
def test_readline(envvars, params):
    downstream = StringIO("\n".join(params["stdin"]))
    upstream = sub(downstream)
    line = upstream.readline()
    assert line == params["expected"][0]
    line = upstream.readline()
    assert line == params["expected"][1]
    line = upstream.readline()
    assert line == ''
    line = upstream.readline()
    assert line == ''


@pytest.mark.parametrize(
    "params",
    [
        pytest.param(
            {
                "envvars": {"name": "Bob", "alt": "Harriet"},
                "stdin": [
                    "Hello, ${name}!",
                    "Hello, also ${alt}!",
                ],
                "expected": [
                    "Hello, Bob!\n",
                    "Hello, also Harriet!",
                ],
            },
            id="all lines",
        ),
    ],
)
def test_readlines(envvars, params):
    downstream = StringIO("\n".join(params["stdin"]))
    upstream = sub(downstream)
    lines = upstream.readlines()
    assert lines == params["expected"]
