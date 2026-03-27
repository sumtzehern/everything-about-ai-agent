"""Utility functions for mypackage."""

from typing import Any


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a numeric value between a minimum and maximum.

    Args:
        value: The number to clamp.
        min_val: The lower bound (inclusive).
        max_val: The upper bound (inclusive).

    Returns:
        The clamped value.

    Raises:
        ValueError: If min_val is greater than max_val.

    Examples:
        >>> clamp(5, 1, 10)
        5
        >>> clamp(-3, 0, 10)
        0
        >>> clamp(15, 0, 10)
        10
    """
    if min_val > max_val:
        raise ValueError(f"min_val ({min_val}) must not be greater than max_val ({max_val})")
    return max(min_val, min(value, max_val))


def flatten(nested: list[Any], depth: int = -1) -> list[Any]:
    """Recursively flatten a nested list up to a given depth.

    Args:
        nested: A (potentially nested) list to flatten.
        depth: How many levels deep to flatten. -1 means fully flatten.

    Returns:
        A new flattened list.

    Examples:
        >>> flatten([1, [2, [3, 4]], 5])
        [1, 2, 3, 4, 5]
        >>> flatten([1, [2, [3, 4]], 5], depth=1)
        [1, 2, [3, 4], 5]
    """
    result: list[Any] = []
    for item in nested:
        if isinstance(item, list) and depth != 0:
            result.extend(flatten(item, depth - 1))
        else:
            result.append(item)
    return result


def is_palindrome(text: str, *, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Check whether a string is a palindrome.

    Args:
        text: The string to check.
        ignore_case: If True, comparison is case-insensitive. Defaults to True.
        ignore_spaces: If True, spaces are stripped before comparison. Defaults to True.

    Returns:
        True if *text* is a palindrome, False otherwise.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    processed = text
    if ignore_case:
        processed = processed.lower()
    if ignore_spaces:
        processed = processed.replace(" ", "")
    return processed == processed[::-1]
