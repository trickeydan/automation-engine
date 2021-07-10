"""MQTT Automate API."""
import argparse
import asyncio
from pathlib import Path
from typing import Optional

from .engine import AutomationEngine

loop = asyncio.get_event_loop()


class MQTTAutomate:
    """MQTT Automation."""

    def app(self, verbose: bool, config_file: Optional[str]) -> None:
        """Main function for MQTTAutomate."""
        mqtt = AutomationEngine(verbose, config_file)
        loop.run_until_complete(mqtt.run())

    def run(self) -> None:
        """Start the automation engine."""
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("-c", "--config-file", type=Path, default=None)
        args = parser.parse_args()
        self.app(args.verbose, args.config_file)
