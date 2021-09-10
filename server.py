#!/usr/bin/env python3

import asyncio
from can import notifier
import ws_data_server
import can
import can_processor
from signal import signal, SIGINT
from sys import exit

def quit(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    loop.stop()
    bus.shutdown()
    bus2.shutdown()
    socTask.stop()
    exit(0)

def init():  
    #virtual interfaces for development
    global bus
    bus = can.interface.Bus('test', bustype='virtual')

    global bus2
    bus2 = can.interface.Bus('test', bustype='virtual')

    global reader
    reader = can.AsyncBufferedReader()

    listeners = [
        reader
    ]

    global notifier
    notifier = can.Notifier(bus, listeners, loop=loop)


def mockCanBus():
    socMessage = can.Message(arbitration_id=0x355, data=[0x3C, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], is_extended_id=False)
    global socTask 
    socTask = bus2.send_periodic(socMessage, 0.50)

    chargeMessage = can.Message(arbitration_id=0x389, data=[0xB0, 0xEB, 0x3C, 0x3D, 0x45, 0xCA, 0x5F, 0x3C], is_extended_id=False)
    global chargeTask 
    chargeTask = bus2.send_periodic(chargeMessage, 0.50)


# Create Notifier with an explicit loop to use for scheduling of callbacks
print('Running. Press CTRL-C to exit.')
signal(SIGINT, quit)
global loop
loop = asyncio.get_event_loop()

init()
can_processor.init()
mockCanBus()
loop.run_until_complete(ws_data_server.init(reader))
loop.run_forever()
