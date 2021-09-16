import asyncio
import json
import logging
import websockets

from .can_processor import CANProcessor

class WebSocketDataServer:
    def __init__(self, config_path, reader):
        self.can_processor = CANProcessor(config_path)
        self.reader = reader


    async def run(self, reader):
        """
            Run the server forever
        """
        print("Web socket server starting on port 6789")
        self.reader = reader
        async with websockets.serve(self.producer_handler, "localhost", 6789):
            await asyncio.Future()  # run forever

    async def producer_handler(self, websocket, path):
        """
        Handle incoming messages
        """
        while True:
            message = await self.reader.get_message()
            response = await self.can_processor.handle_message(message)
            await websocket.send(json.dumps(response))
