"""MQTT Automate API."""
import argparse
import asyncio
import logging
from pathlib import Path
from typing import Callable, Dict, Match, Optional

from .engine import Engine, OnMessageHandler
from .mqtt import Topic

loop = asyncio.get_event_loop()
LOGGER = logging.getLogger(__name__)


class EngineRunner:
    """Automation Engine Runner."""

    def __init__(self) -> None:
        self._handlers: Dict[Topic, OnMessageHandler] = {}

    def app(self, verbose: bool, config_file: Optional[str]) -> None:
        """Main function for MQTTAutomate."""
        mqtt = Engine(verbose, config_file, self._handlers)
        loop.run_until_complete(mqtt.run())

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
                engine: Engine,
                match: Match[str],
                payload: str,
            ) -> None:
                LOGGER.info(f"INVOKE {topic} -> {func.__name__}")
                await func(engine, match, payload)

            # Register handler
            self._handlers[Topic.parse(topic)] = wrapper
            return wrapper
        return decorator
