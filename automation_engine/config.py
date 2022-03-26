"""
Configuration schema for Automation Engine.

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
    topic_prefix: str = "automation-engine"
    force_protocol_version_3_1: bool = False

    class Config:
        """Pydantic config."""

        extra = "forbid"


class AutomationEngineConfig(BaseModel):
    """Config schema for Automation Engine."""

    mqtt: MQTTBrokerInfo
    name: str

    class Config:
        """Pydantic config."""

        extra = "forbid"

    @classmethod
    def _get_config_path(cls, config_str: Optional[str] = None) -> Path:
        """Check for a config file or search the filesystem for one."""
        CONFIG_SEARCH_PATHS = [
            Path("automation-engine.toml"),
            Path("/etc/automation-engine.toml"),
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
    def load(cls, config_str: Optional[str] = None) -> 'AutomationEngineConfig':
        """Load the config."""
        config_path = cls._get_config_path(config_str)
        with config_path.open("r") as fh:
            return cls.load_from_file(fh)

    @classmethod
    def load_from_file(cls, fh: IO[str]) -> 'AutomationEngineConfig':
        """Load the config from a file."""
        return cls(**load(fh))
