#!/usr/bin/env python3

import asyncio
import websockets
from signal import signal, SIGINT
from sys import exit

def quit(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(response)

signal(SIGINT, quit)
asyncio.get_event_loop().run_until_complete(client())