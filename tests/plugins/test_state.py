"""Test the state plugin."""

import pytest

from automation_engine.plugins.state import StatePlugin


class TestStatePlugin:
    """Test the state plugin."""

    @pytest.fixture
    def state_plugin(self) -> StatePlugin:
        """Get an instance of the state plugin."""
        return StatePlugin(None, None)  # type: ignore

    def test_set_state(self, state_plugin: StatePlugin) -> None:
        """Test that we can set the state."""
        state_plugin.set("bees", True)
        assert state_plugin._state["bees"] is True

    def test_get_state(self, state_plugin: StatePlugin) -> None:
        """Test that we can get the state."""
        state_plugin._state = {"yeet": 13}
        assert state_plugin.get("yeet") == 13

    def test_change_state(self, state_plugin: StatePlugin) -> None:
        """Test that we can chamhe the state."""
        state_plugin._state = {"yeet": 13}
        assert state_plugin.get("yeet") == 13
        state_plugin.set("yeet", 14)
        assert state_plugin.get("yeet") == 14

    def test_get_unknown_key(self, state_plugin: StatePlugin) -> None:
        """Test that we handle a key that doesn't exist."""
        assert state_plugin.get("veee") is None
