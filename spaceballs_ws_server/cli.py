import os
from pathlib import Path
import click
from signal import signal, SIGINT

from spaceballs_ws_server.can_server import CANServer
from spaceballs_ws_server.client import WSClient

location = os.path.dirname(os.path.abspath(__file__))
default_config = os.path.join(location, '..', 'data', 'configs', 'simple.json')

def start_cli():
    cli()


@click.group()
def cli():
    pass

@cli.command()
@click.option('--config', type=click.Path(), default=default_config)
@click.option('--virtual', is_flag=True, flag_value="virtual", default="socketcan_native",
    help="A flag to create a virtual can interface, otherwise it expects an active can bus on 'can0'")
def run(config, virtual):
    """
    Create Notifier with an explicit loop to use for scheduling of callbacks
    """
    print('Running. Press CTRL-C to exit.')

    ws_server = CANServer(config, bustype=virtual)

    signal(SIGINT, quit)

    ws_server.run()

@cli.command()
def run_client():
    """
    Run a WS client to check that data is being sent properly
    """
    print('Running Client. Press CTRL-C to exit.')

    ws_client = WSClient()

    ws_client.run()
