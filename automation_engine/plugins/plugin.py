"""A Plugin for Automation Engine."""

import logging
from abc import ABCMeta
from typing import Any, Dict, List, Type, TypeVar

from automation_engine.mqtt import MQTTWrapper

PluginT = TypeVar("PluginT", bound=Type['Plugin'])

LOGGER = logging.getLogger(__name__)


class PluginManager:
    """Class to hold all currently loaded plugins."""

    def __init__(self, plugins: List[PluginT], mqtt: MQTTWrapper) -> None:
        self._plugins: Dict[str, Plugin] = {}

        for plugin_class in plugins:
            instance = plugin_class(mqtt)
            LOGGER.info(f"Registering plugin {plugin_class.name}")
            self._plugins[str(plugin_class.name)] = instance

    def __getattr__(self, __name: str) -> Any:
        if __name in self._plugins:
            return self._plugins[__name]
        else:
            raise ValueError(f"Unknown plugin: {__name}")


class Plugin(metaclass=ABCMeta):
    """A Plugin for Automation Engine."""

    def __init__(self, mqtt: MQTTWrapper) -> None:
        pass

    @property
    def name(self) -> str:
        """The name of the plugin."""
        raise NotImplementedError
