"""Application entrypoint."""
import asyncio
from typing import Optional

import click

from .mqtt_automate import MQTTAutomate

loop = asyncio.get_event_loop()


@click.command("mqtt-automate")
@click.option("-v", "--verbose", is_flag=True)
@click.option("-c", "--config-file", type=click.Path(exists=True))
def app(*, verbose: bool, config_file: Optional[str]) -> None:
    """Main function for MQTTAutomate."""
    mqtt = MQTTAutomate(verbose, config_file)
    loop.run_until_complete(mqtt.run())


if __name__ == "__main__":
    app()
