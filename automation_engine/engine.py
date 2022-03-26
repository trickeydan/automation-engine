"""Automation Engine."""
import asyncio
import logging
import signal
import sys
from functools import partial
from signal import SIGHUP, SIGINT, SIGTERM
from types import FrameType
from typing import Any, Callable, Coroutine, Dict, Match, Optional

from .config import AutomationEngineConfig
from .mqtt.topic import Topic
from .mqtt.wrapper import MQTTWrapper
from .version import __version__

try:
    from .hue import HueWrapper
    HUE = True
except Exception:
    HUE = False


LOGGER = logging.getLogger(__name__)

loop = asyncio.get_event_loop()

OnMessageHandler = Callable[
    ['Engine', Match[str], str],
    Coroutine[Any, Any, None],
]


class Engine:
    """Home Automation Engine powered by MQTT."""

    config: AutomationEngineConfig

    def __init__(
        self,
        verbose: bool,
        config_file: Optional[str],
        handlers: Dict[Topic, OnMessageHandler],
    ) -> None:
        self.config = AutomationEngineConfig.load(config_file)
        self.name = self.config.name

        self._setup_logging(verbose)
        self._setup_event_loop()
        self._setup_mqtt()
        self._setup_handlers(handlers)

        if HUE:
            self.hue = HueWrapper(self._mqtt)

        self.wait_event = asyncio.Event()

    def _setup_logging(self, verbose: bool) -> None:
        if verbose:
            logging.basicConfig(
                level=logging.DEBUG,
                format=f"%(asctime)s {self.name} %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        else:
            logging.basicConfig(
                level=logging.INFO,
                format=f"%(asctime)s {self.name} %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # Suppress INFO messages from gmqtt
            logging.getLogger("gmqtt").setLevel(logging.WARNING)

        LOGGER.info(f"Automation Engine v{__version__} - {self.__doc__}")

    def _setup_event_loop(self) -> None:
        loop.add_signal_handler(SIGHUP, self.halt)
        loop.add_signal_handler(SIGINT, self.halt)
        loop.add_signal_handler(SIGTERM, self.halt)

    def _setup_mqtt(self) -> None:
        self._mqtt = MQTTWrapper(
            self.name,
            self.config.mqtt,
        )

    def _setup_handlers(self, handlers: Dict[Topic, OnMessageHandler]) -> None:
        """Setup the topic handlers."""
        for topic, handler in handlers.items():
            LOGGER.info(f"Registering action {handler.__name__} on {topic}")
            final_handler = partial(handler, self)
            final_handler.__name__ = handler.__name__  # type: ignore
            self._mqtt.subscribe(str(topic), final_handler, no_prefix=True)

    def _exit(self, signals: signal.Signals, frame_type: FrameType) -> None:
        sys.exit(0)

    async def run(self) -> None:
        """Entrypoint for the data component."""
        await self._mqtt.connect()
        LOGGER.info("Connected to MQTT Broker")

        await self.wait_event.wait()

        await self._mqtt.disconnect()

    def halt(self) -> None:
        """Stop the component."""
        self.wait_event.set()
        sys.exit(-1)
