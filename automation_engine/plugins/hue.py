"""Hue2MQTT Wrapper."""
import json
import logging
from typing import Any, Dict, Match

from hue2mqtt.schema import GroupInfo, GroupSetState, LightInfo, LightSetState
from pydantic import ValidationError

from automation_engine.mqtt import MQTTWrapper

from .plugin import Plugin

LOGGER = logging.getLogger(__name__)


class HuePlugin(Plugin):
    """Plugin to wrap Hue2MQTT."""

    name = "hue"

    def __init__(self, mqtt: MQTTWrapper) -> None:
        self._mqtt = mqtt
        self.lights: Dict[str, LightInfo] = {}
        self.groups: Dict[int, GroupInfo] = {}

        self._mqtt.subscribe("hue2mqtt/light/+", self._handle_light_event, no_prefix=True)
        self._mqtt.subscribe("hue2mqtt/group/+", self._handle_group_event, no_prefix=True)

    async def _handle_light_event(self, match: Match[str], payload: str) -> None:
        uniqueid = match.group(1)
        try:
            light = LightInfo(**json.loads(payload))
            if light.uniqueid == uniqueid:
                LOGGER.info(f"Updating light: {light.name}({light.uniqueid})")
                self.lights[light.uniqueid] = light
            else:
                LOGGER.warning("Light event uniqueid didn't match object")
        except json.JSONDecodeError:
            LOGGER.warning("Invalid JSON received for light event")
        except ValidationError as e:
            LOGGER.warning(f"Light info did not match schema {e}")

    async def _handle_group_event(self, match: Match[str], payload: str) -> None:
        groupid = match.group(1)
        try:
            group = GroupInfo(**json.loads(payload))
            if group.id == int(groupid):
                LOGGER.info(f"Updating group: {group.name}({group.id})")
                self.groups[group.id] = group
            else:
                LOGGER.warning("Group event uniqueid didn't match object")
        except json.JSONDecodeError:
            LOGGER.warning("Invalid JSON received for group event")
        except ValidationError as e:
            LOGGER.warning(f"Group info did not match schema {e}")

    def set_group(self, group: int, **kwargs: Any) -> None:
        """Set the state of a group in Hue."""
        state = GroupSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/group/{group}/set",
            state,
            auto_prefix_topic=False,
        )

    def toggle_group(self, group: int) -> None:
        """Toggle the state of a group."""
        if group in self.groups:
            group_info = self.groups[group]
            toggle_state = not group_info.action.on
            LOGGER.info(f"Toggling {group_info.name} to {toggle_state}")
            self.set_group(group, on=toggle_state)
        else:
            LOGGER.warning(f"Attempted to toggle group {group}, but no info available.")

    def set_light(self, light: str, **kwargs: Any) -> None:
        """Set the state of a light in Hue."""
        state = LightSetState(**kwargs)
        self._mqtt.publish(
            f"hue2mqtt/light/{light}/set",
            state,
            auto_prefix_topic=False,
        )

    def toggle_light(self, light: str) -> None:
        """Toggle the state of a light."""
        if light in self.lights:
            light_info = self.lights[light]
            if light_info.state:
                toggle_state = not light_info.state.on
                LOGGER.info(f"Toggling {light_info.name} to {toggle_state}")
                self.set_light(light, on=toggle_state)
                return
        LOGGER.warning(f"Attempted to toggle light {light}, but no info available.")
