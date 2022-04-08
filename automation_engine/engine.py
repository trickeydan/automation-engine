"""Automation Engine API."""
import argparse
import asyncio
import json
import logging
from pathlib import Path
from typing import Callable, Dict, List, Match, Optional

from .mqtt import Topic
from .piston import OnMessageHandler, Piston, PluginT

loop = asyncio.get_event_loop()
LOGGER = logging.getLogger(__name__)


class AutomationEngine:
    """Home Automation Engine powered by MQTT."""

    def __init__(self, plugins: List[PluginT]) -> None:
        self._plugins = plugins
        self._handlers: Dict[Topic, OnMessageHandler] = {}

    def app(self, verbose: bool, config_file: Optional[str]) -> None:
        """Main function for Automation Engine."""
        piston = Piston(verbose, config_file, self._handlers, plugins=self._plugins)
        loop.run_until_complete(piston.run())

    def run(self) -> None:
        """Start the automation engine."""
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("-c", "--config-file", type=Path, default=None)
        args = parser.parse_args()
        self.app(args.verbose, args.config_file)

    def on_message(self, topic: str) -> Callable[[OnMessageHandler], OnMessageHandler]:
        """Register a topic to react to."""
        def decorator(func: OnMessageHandler) -> OnMessageHandler:

            async def wrapper(
                piston: Piston,
                match: Match[str],
                payload: str,
            ) -> None:
                LOGGER.info(f"INVOKE {topic} -> {func.__name__}")
                await func(piston, match, payload)

            # Register handler
            self._handlers[Topic.parse(topic)] = wrapper
            return wrapper
        return decorator

    def on_json(self, topic: str) -> Callable[[OnMessageHandler], OnMessageHandler]:
        """Register a topic to decode as JSON and react to."""
        def decorator(func: OnMessageHandler) -> OnMessageHandler:

            async def wrapper(
                piston: Piston,
                match: Match[str],
                payload: str,
            ) -> None:
                LOGGER.info(f"JSON {topic} -> {func.__name__}")
                try:
                    data = json.loads(payload)
                    await func(piston, match, data)
                except json.JSONDecodeError as e:
                    LOGGER.warning(f"Unable to decode JSON: {e}")

            # Register handler
            self._handlers[Topic.parse(topic)] = wrapper
            return wrapper
        return decorator
