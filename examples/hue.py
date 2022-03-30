"""Automation Engine Example to trigger Hue Lights."""
import logging
from typing import Any, Match

from automation_engine import Engine, EngineRunner
from automation_engine.plugins.hue import HuePlugin

LOGGER = logging.getLogger(__name__)

automate = EngineRunner(plugins=[HuePlugin])

# Zigbee2MQTT Names
LANDING_SWITCH = "switch_03"

# Hue Group IDs
GROUP_STAIRWELL = 10


@automate.on_message(f"zigbee2mqtt/{LANDING_SWITCH}/action")
async def landing_switch_action(
    engine: Engine,
    match: Match[str],
    payload: str,
) -> None:
    """Do things when the landing switch is pressed."""
    LOGGER.info(f"Landing switch: {payload}")

    if payload == "on":
        # Turn on the stairwell lights
        engine.plugins.hue.set_group(GROUP_STAIRWELL, on=True)
    elif payload == "off":
        # Turn off the stairwell lights
        engine.plugins.hue.set_group(GROUP_STAIRWELL, on=False)


@automate.on_json(f"zigbee2mqtt/{LANDING_SWITCH}/json")
async def landing_switch_json(
    engine: Engine,
    match: Match[str],
    payload: Any,
) -> None:
    """Do things when the landing switch is pressed."""
    LOGGER.info(f"Landing switch: {payload}")

    if payload["action"] == "on":
        # Turn on the stairwell lights
        engine.plugins.hue.set_group(GROUP_STAIRWELL, on=True)
    elif payload["action"] == "off":
        # Turn off the stairwell lights
        engine.plugins.hue.set_group(GROUP_STAIRWELL, on=False)

automate.run()