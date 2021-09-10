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
    #Dont break on a match, a single ID might have multiple messages we're interested in
    for c in config:
        if (msg.arbitration_id == c['id']):
            value = globals()[c['transformer']](msg, c)
    
    if c.get("scale") != None:
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

def value_map(msg, config):
    #unpack to one big number
    fmt = '<q'
    value = struct.unpack(fmt, msg.data)[0]

    #mask off the required bytes
    mask = config['length'] << config['start'] - 2
    hex = (value & mask) >> config['start'] - 2

    #lookup result
    for k,v in config["map"].items():
        if hex == int(k, 16):
            return v
    return "0x" + str(hex)