"""A Plugin for Automation Engine."""

import logging
from abc import ABCMeta
from typing import Any, Dict, List, Type, TypeVar

from pydantic import BaseModel, ValidationError, parse_obj_as

from automation_engine.config import AutomationEngineConfig
from automation_engine.mqtt import MQTTWrapper

PluginT = TypeVar("PluginT", bound=Type['Plugin'])

LOGGER = logging.getLogger(__name__)


class PluginManager:
    """Class to hold all currently loaded plugins."""

    def __init__(
        self,
        plugins: List[PluginT],
        config: AutomationEngineConfig,
        mqtt: MQTTWrapper,
    ) -> None:
        self._plugins: Dict[str, Plugin] = {}

        for plugin_class in plugins:
            plugin_name = str(plugin_class.name)
            config_data = config.plugins.get(plugin_name, {})
            try:
                plugin_config = parse_obj_as(plugin_class.Config, config_data)
                instance = plugin_class(mqtt, plugin_config)
                LOGGER.info(f"Registering plugin {plugin_class.name}")
                self._plugins[plugin_name] = instance
            except ValidationError as e:
                LOGGER.error(
                    f"Unable to load plugin {plugin_name} as the config is invalid!",
                )
                LOGGER.error(str(e))

    def __getattr__(self, __name: str) -> Any:
        if __name in self._plugins:
            return self._plugins[__name]
        else:
            raise ValueError(f"Unknown plugin: {__name}")


class Plugin(metaclass=ABCMeta):
    """A Plugin for Automation Engine."""

    class Config(BaseModel):
        """Base Config Schema for a Plugin."""

    def __init__(self, mqtt: MQTTWrapper, config: Config) -> None:
        pass

    @property
    def name(self) -> str:
        """The name of the plugin."""
        raise NotImplementedError
