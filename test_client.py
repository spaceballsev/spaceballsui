#!/usr/bin/env python3

import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            print(response)
        
asyncio.get_event_loop().run_until_complete(client())