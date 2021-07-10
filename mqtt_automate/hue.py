"""Hue2MQTT Wrapper."""
from typing import Any

from hue2mqtt.schema import LightSetState

from .mqtt.wrapper import MQTTWrapper


class HueWrapper:
    """Wrap Hue2MQTT."""

    def __init__(self, mqtt: MQTTWrapper) -> None:
        self._mqtt = mqtt

    def set_group(self, group: int, **kwargs: Any) -> None:
        """Set the state of a group in Hue."""
        state = LightSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/group/{group}/set",
            state,
            auto_prefix_topic=False,
        )

    def set_light(self, light: str, **kwargs: Any) -> None:
        """Set the state of a light in Hue."""
        state = LightSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/light/{light}/set",
            state,
            auto_prefix_topic=False,
        )
