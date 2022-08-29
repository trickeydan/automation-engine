"""Automation Engine API."""
import argparse
import asyncio
import json
import logging
from pathlib import Path
from typing import Callable, Dict, List, Match, Optional

from prometheus_client import Counter

from .mqtt import Topic
from .piston import OnMessageHandler, Piston, PluginT

loop = asyncio.get_event_loop()
LOGGER = logging.getLogger(__name__)


AUTOMATIONS_TRIGGERED = Counter(
    'automation_engine_invoked',
    'Number of invoked automations',
    ['name', 'data_type'],
)
AUTOMATIONS_BAD_JSON = Counter(
    'automation_engine_bad_json',
    'Number of invoked JSON triggers with bad JSON',
    ['name'],
)


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
                AUTOMATIONS_TRIGGERED.labels(name=func.__name__, data_type="str").inc()
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
                name = func.__name__
                LOGGER.info(f"JSON {topic} -> {name}")
                try:
                    data = json.loads(payload)
                    AUTOMATIONS_TRIGGERED.labels(name=name, data_type='json').inc()
                    await func(piston, match, data)
                except json.JSONDecodeError as e:
                    AUTOMATIONS_BAD_JSON.labels(name=name).inc()
                    LOGGER.warning(f"Unable to decode JSON: {e}")

            # Register handler
            self._handlers[Topic.parse(topic)] = wrapper
            return wrapper
        return decorator
