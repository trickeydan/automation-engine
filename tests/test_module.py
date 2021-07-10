"""Test that the MQTTAutomate imports as expected."""

import mqtt_automate


def test_module() -> None:
    """Test that the module behaves as expected."""
    assert mqtt_automate.__version__ is not None
