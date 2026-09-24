import pytest

import validate_b


def test_valid_email_normal_address():
    assert validate_b.is_valid_email("first.last@example.co.uk") is True


def test_invalid_email_missing_dot_after_at():
    assert validate_b.is_valid_email("user@example") is False


def test_invalid_email_too_long():
    assert validate_b.is_valid_email("a" * 300 + "@example.com") is False


def test_invalid_email_with_space_in_local_part():
    assert validate_b.is_valid_email("user name@example.com") is False
