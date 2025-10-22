"""
Utility functions to generate short unique identifiers.

This module exposes:
- generate_unique_id(): returns a short identifier derived from uuid4.

Note: the returned IDs are short (4 characters by default) and therefore
not collision-proof. Use full UUIDs when strong uniqueness is required.
"""

import uuid

def generate_unique_id() -> str:
    """
    Generate a short unique identifier derived from a UUID4.

    The function creates a UUID4 and returns a small substring of its string
    representation. This is convenient for human-friendly short IDs but is
    not guaranteed to be globally unique; collisions are possible.

    Returns
    -------
    str
        A short identifier string (4 characters).
    """
    base = str(uuid.uuid4())
    id = base[9:13]
    return id