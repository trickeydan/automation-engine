"""Test that Automation Engine imports as expected."""

import automation_engine


def test_module() -> None:
    """Test that the module behaves as expected."""
    assert automation_engine.__version__ is not None
