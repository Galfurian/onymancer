"""Procedural fantasy name generation library."""

__version__ = "0.1.0"

from .namegen import (
    generate,
    load_tokens_from_json,
    set_token,
    set_tokens,
)

__all__ = [
    "generate",
    "load_tokens_from_json",
    "set_token",
    "set_tokens",
]
