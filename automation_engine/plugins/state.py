"""A plugin that holds state."""
import logging
import threading
from typing import Any, Dict, Optional

from automation_engine.mqtt import MQTTWrapper

from .plugin import Plugin

LOGGER = logging.getLogger(__name__)


class StatePlugin(Plugin):
    """A plugin that holds state."""

    name = "state"

    class Config(Plugin.Config):
        """State Plugin Config Schema."""

    def __init__(self, mqtt: MQTTWrapper, config: Config) -> None:
        self._lock = threading.Lock()
        self._state: Dict[str, Any] = {}

    def set(self, key: str, val: Any) -> None:
        """Set a state."""
        with self._lock:
            self._state[key] = val

    def get(self, key: str) -> Optional[Any]:
        """Get the state for a key."""
        with self._lock:
            return self._state.get(key)
