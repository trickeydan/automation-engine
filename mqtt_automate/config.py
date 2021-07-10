"""
Configuration schema for MQTTAutomate.

Common to all components.
"""
from pathlib import Path
from typing import IO, Optional

from pydantic import BaseModel
from toml import load


class MQTTBrokerInfo(BaseModel):
    """MQTT Broker Information."""

    host: str
    port: int
    enable_tls: bool = False
    topic_prefix: str = "mqtt-automate"
    force_protocol_version_3_1: bool = False

    class Config:
        """Pydantic config."""

        extra = "forbid"


class MQTTAutomateConfig(BaseModel):
    """Config schema for MQTTAutomate."""

    mqtt: MQTTBrokerInfo

    class Config:
        """Pydantic config."""

        extra = "forbid"

    @classmethod
    def _get_config_path(cls, config_str: Optional[str] = None) -> Path:
        """Check for a config file or search the filesystem for one."""
        CONFIG_SEARCH_PATHS = [
            Path("mqtt-automate.toml"),
            Path("/etc/mqtt-automate.toml"),
        ]
        if config_str is None:
            for path in CONFIG_SEARCH_PATHS:
                if path.exists() and path.is_file():
                    return path
        else:
            path = Path(config_str)
            if path.exists() and path.is_file():
                return path
        raise FileNotFoundError("Unable to find config file.")

    @classmethod
    def load(cls, config_str: Optional[str] = None) -> 'MQTTAutomateConfig':
        """Load the config."""
        config_path = cls._get_config_path(config_str)
        with config_path.open("r") as fh:
            return cls.load_from_file(fh)

    @classmethod
    def load_from_file(cls, fh: IO[str]) -> 'MQTTAutomateConfig':
        """Load the config from a file."""
        return cls(**load(fh))
