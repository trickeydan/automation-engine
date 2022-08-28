"""Test that we load configs correctly."""
from pathlib import Path

import pydantic
import pytest

from automation_engine.config import AutomationEngineConfig

DATA_DIR = Path(__file__).resolve().parent.joinpath("data/configs")


def test_valid_config() -> None:
    """Test that we can load a valid config from a file."""
    with DATA_DIR.joinpath("valid.toml").open("rb") as fh:
        config = AutomationEngineConfig.load_from_file(fh)
    assert config is not None


def test_invalid_config() -> None:
    """Test that we cannot load an invalid config."""
    with DATA_DIR.joinpath("invalid.toml").open("rb") as fh:
        with pytest.raises(pydantic.ValidationError):
            AutomationEngineConfig.load_from_file(fh)
