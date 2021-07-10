"""Hue2MQTT Wrapper."""

from hue2mqtt.schema import LightSetState

from .mqtt.wrapper import LOGGER, MQTTWrapper

class HueWrapper:

    def __init__(self, mqtt: MQTTWrapper) -> None:
        self._mqtt = mqtt

    def set_group(self, group: int, **kwargs) -> None:
        state = LightSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/group/{group}/set",
            state,
            auto_prefix_topic=False,
        )

    def set_light(self, light: str, **kwargs) -> None:
        state = LightSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/light/{light}/set",
            state,
            auto_prefix_topic=False,
        )