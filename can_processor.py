import json
import json
import struct

def init():
    with open('config.json', 'r') as myfile:
        data=myfile.read()

    # parse file
    global config
    config = json.loads(data)

async def handleMessage(msg):
    for c in config:
        if (msg.arbitration_id == c['id']):
            value = globals()[c['transformer']](msg, c)
            break
    
    if c['scale']:
        value = value * c['scale']

    response = {
        'key': c['key'],
        'unit': c['unit'],
        'value': value
    }
    
    return response

def unpack(msg, config, str):
    start = config['start']
    length = config['length']
    if length == 16:
        str = str + 'i'
    elif length == 8:
        str = str + 'B'

    return struct.unpack_from(str, msg.data, int(start/8))[0]

def little_endian(msg, config):
    str = '<'
    return unpack(msg, config, str)
   

def big_endian(msg, config):
    str = '>'
    return unpack(msg, config, str)