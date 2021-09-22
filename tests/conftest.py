import os
import pytest
from spaceballs_ws_server.can_server import CANServer
from spaceballs_ws_server.client import WSClient



@pytest.fixture(scope="session")
def ws_client():
    return WSClient()


@pytest.fixture(scope="session")
def can_server():
    current_folder = os.path.dirname(os.path.expanduser(__file__))
    config_path = os.path.join(current_folder, '..', 'data', 'configs', 'simple.json')

    return CANServer(config_path, bustype="virtual")

@pytest.fixture(scope="session")
def event_loop(can_server):
    yield can_server.loop
    can_server.loop.close()
