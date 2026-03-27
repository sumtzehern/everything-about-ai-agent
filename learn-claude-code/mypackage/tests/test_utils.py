"""Tests for mypackage.utils."""

import pytest

from mypackage.utils import clamp, flatten, is_palindrome


# ---------------------------------------------------------------------------
# clamp
# ---------------------------------------------------------------------------

class TestClamp:
    def test_value_within_range(self) -> None:
        assert clamp(5, 1, 10) == 5

    def test_value_below_min(self) -> None:
        assert clamp(-3, 0, 10) == 0

    def test_value_above_max(self) -> None:
        assert clamp(15, 0, 10) == 10

    def test_value_equals_min(self) -> None:
        assert clamp(0, 0, 10) == 0

    def test_value_equals_max(self) -> None:
        assert clamp(10, 0, 10) == 10

    def test_float_values(self) -> None:
        assert clamp(1.5, 1.0, 2.0) == 1.5

    def test_invalid_range_raises(self) -> None:
        with pytest.raises(ValueError, match="min_val"):
            clamp(5, 10, 1)


# ---------------------------------------------------------------------------
# flatten
# ---------------------------------------------------------------------------

class TestFlatten:
    def test_already_flat(self) -> None:
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_fully_nested(self) -> None:
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

    def test_depth_one(self) -> None:
        assert flatten([1, [2, [3, 4]], 5], depth=1) == [1, 2, [3, 4], 5]

    def test_depth_zero_unchanged(self) -> None:
        assert flatten([1, [2, 3]], depth=0) == [1, [2, 3]]

    def test_empty_list(self) -> None:
        assert flatten([]) == []

    def test_deeply_nested(self) -> None:
        assert flatten([[[[1]]]]) == [1]

    def test_mixed_types(self) -> None:
        assert flatten([1, ["a", [True, None]]]) == [1, "a", True, None]


# ---------------------------------------------------------------------------
# is_palindrome
# ---------------------------------------------------------------------------

class TestIsPalindrome:
    def test_simple_palindrome(self) -> None:
        assert is_palindrome("racecar") is True

    def test_simple_non_palindrome(self) -> None:
        assert is_palindrome("hello") is False

    def test_case_insensitive_by_default(self) -> None:
        assert is_palindrome("Racecar") is True

    def test_case_sensitive(self) -> None:
        assert is_palindrome("Racecar", ignore_case=False) is False

    def test_phrase_with_spaces(self) -> None:
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_spaces_respected_when_not_ignored(self) -> None:
        assert is_palindrome("race car", ignore_spaces=False) is False

    def test_empty_string(self) -> None:
        assert is_palindrome("") is True

    def test_single_character(self) -> None:
        assert is_palindrome("x") is True
