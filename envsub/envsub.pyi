"""Pyo3 binding interface definition."""

from typing import TextIO


def sub(downstream: TextIO) -> TextIO:
    """
    Replace all the envar from a downstream and return an upstream.

    :downstream: A file-like object that provides text input.
    :return: A file-like object with environment variables replaced.
    """
