"""Automation Engine Example to trigger Hue Lights."""
import logging
from typing import Any, Match

from automation_engine import AutomationEngine, Piston
from automation_engine.plugins.hue import HuePlugin

LOGGER = logging.getLogger(__name__)

engine = AutomationEngine(plugins=[HuePlugin])

# Zigbee2MQTT Names
LANDING_SWITCH = "switch_03"

# Hue Group IDs
GROUP_STAIRWELL = 10


@engine.on_message(f"zigbee2mqtt/{LANDING_SWITCH}/action")
async def landing_switch_action(
    piston: Piston,
    match: Match[str],
    payload: str,
) -> None:
    """Do things when the landing switch is pressed."""
    LOGGER.info(f"Landing switch: {payload}")

    if payload == "on":
        # Turn on the stairwell lights
        piston.plugins.hue.set_group(GROUP_STAIRWELL, on=True)
    elif payload == "off":
        # Turn off the stairwell lights
        piston.plugins.hue.set_group(GROUP_STAIRWELL, on=False)


@engine.on_json(f"zigbee2mqtt/{LANDING_SWITCH}/json")
async def landing_switch_json(
    piston: Piston,
    match: Match[str],
    payload: Any,
) -> None:
    """Do things when the landing switch is pressed."""
    LOGGER.info(f"Landing switch: {payload}")

    if payload["action"] == "on":
        # Turn on the stairwell lights
        piston.plugins.hue.set_group(GROUP_STAIRWELL, on=True)
    elif payload["action"] == "off":
        # Turn off the stairwell lights
        piston.plugins.hue.set_group(GROUP_STAIRWELL, on=False)

engine.run()
