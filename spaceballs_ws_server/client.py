#!/usr/bin/env python3

import asyncio
import websockets
from signal import signal, SIGINT
from sys import exit


class WSClient:
    """
    Web socket client, used primarily for testing
    """

    def __init__(self, host='localhost', port=6789):
        self.port = port
        self.host = host
        self.uri = f"ws://{host}:{port}"

        print(f"Connected to: {self.uri}")

    def quit(self, signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        exit(0)

    async def client(self):
        async with websockets.connect(self.uri) as websocket:
            while True:
                response = await websocket.recv()
                print(response)

    def run(self):
        signal(SIGINT, self.quit)
        asyncio.get_event_loop().run_until_complete(self.client())
