#!/usr/bin/env python3
from sys import exit
from signal import signal, SIGINT

import asyncio
import can
from spaceballs_ws_server.ws_data_server import WebSocketDataServer


class CANServer:

    def quit(self, signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        self.loop.stop()
        self.bus.shutdown()
        self.bus2.shutdown()

        for t in self.tasks:
            t.stop()

        exit(0)

    def __init__(self, config_path):
        #virtual interfaces for development
        self.bus = can.interface.Bus('test', bustype='virtual')

        self.bus2 = can.interface.Bus('test', bustype='virtual')

        self.reader = can.AsyncBufferedReader()

        self.listeners = [
            self.reader
        ]

        self.tasks = [] # stores messges being sent

        self.loop = asyncio.get_event_loop()

        self.notifier = can.Notifier(self.bus, self.listeners, loop=self.loop)

        self.web_socket_server = WebSocketDataServer(config_path, self.reader)

    def run(self):
        """
        Run the server
        """
        self.loop.run_until_complete(self.web_socket_server.run(self.reader))
        self.loop.run_forever()

    def mockCanBus(self):
        """
        Create some test messages. TODO: MOve this to a proper unit test.
        """
        socMessage = can.Message(
            arbitration_id=0x355,
            data=[0x3C, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0],
            is_extended_id=False)
        self.tasks.append(self.bus2.send_periodic(socMessage, 0.50))

        chargeMessage = can.Message(
            arbitration_id=0x389,
            data=[0xB0, 0xEB, 0x3C, 0x3D, 0x45, 0xCA, 0x5F, 0x3C],
            is_extended_id=False)
            
        self.tasks.append(self.bus2.send_periodic(chargeMessage, 0.50))
