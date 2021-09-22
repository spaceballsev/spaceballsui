import asyncio
import json
import logging
import websockets

from .can_processor import CANProcessor

class WebSocketDataServer:
    def __init__(self, config_path, reader, loop, host="localhost", port=6789):
        self.can_processor = CANProcessor(config_path)
        self.reader = reader
        self.host = host
        self.port = port
        self.loop = loop
        self.uri = f'ws://{self.host}:{self.port}'

    async def run(self):
        """
            Run the server forever
        """
        print("Web socket server starting on port 6789")
        async with websockets.serve(self.producer_handler, self.host, self.port):
            await self.loop.create_future()  # run forever

    async def producer_handler(self, websocket, path):
        """
        Handle incoming messages, process them and then relay the processed data
        on a web socket.
        """
        while True:
            message = await self.reader.get_message()
            response = await self.can_processor.handle_message(message)
            await websocket.send(json.dumps(response))
