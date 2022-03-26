"""Automation Engine Example."""
import logging
from typing import Match

from automation_engine import Engine, EngineRunner

LOGGER = logging.getLogger(__name__)

automate = EngineRunner()

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
        engine.hue.set_group(GROUP_STAIRWELL, on=True)
    elif payload == "off":
        # Turn off the stairwell lights
        engine.hue.set_group(GROUP_STAIRWELL, on=False)

automate.run()
