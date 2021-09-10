import asyncio
import json
import can_processor
import websockets

connected = set()
async def init(tete):
    global reader
    reader = tete
    async with websockets.serve(producer_handler, "localhost", 6789):
        await asyncio.Future()  # run forever

async def producer_handler(websocket, path):
    while True:
        message = await reader.get_message()
        response = await can_processor.handleMessage(message)
        await websocket.send(json.dumps(response))