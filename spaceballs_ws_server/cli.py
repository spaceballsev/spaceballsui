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
def test(config):
    """
    Create Notifier with an explicit loop to use for scheduling of callbacks
    """
    print('Running. Press CTRL-C to exit.')

    ws_server = CANServer(config)

    signal(SIGINT, quit)

    ws_server.mockCanBus() #TODO: Put this into pytest, not here.

    ws_server.run()

@cli.command()
@click.option('--config', type=click.Path(), default=default_config)
def run(config):
    """
    Create Notifier with an explicit loop to use for scheduling of callbacks
    """
    print('Running. Press CTRL-C to exit.')

    ws_server = CANServer(config)

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
