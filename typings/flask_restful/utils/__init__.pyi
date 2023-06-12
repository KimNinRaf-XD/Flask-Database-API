"""
This type stub file was generated by pyright.
"""

import sys
from collections.abc import OrderedDict
from werkzeug.http import HTTP_STATUS_CODES

PY3 = ...
def http_status_message(code): # -> str:
    """Maps an HTTP status code to the textual status"""
    ...

def unpack(value): # -> tuple[Unknown, Literal[200], dict[Unknown, Unknown]] | tuple[Unknown, Unknown, Unknown] | tuple[Unknown, Unknown, dict[Unknown, Unknown]] | tuple[tuple[Unknown, ...], Literal[200], dict[Unknown, Unknown]]:
    """Return a three tuple of data, code, and headers"""
    ...
