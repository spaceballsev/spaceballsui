# spaceballsui
A web socket server which consumes CAN messages, processes them, and the processed
data to a web socket for use in a display

## Installation
### For Development:
```bash
python setup.py develop
```
### For Release:
```bash
python setup.py install
```

## Usage:

```bash
$ spaceballs run
```
or

```bash
$ spaceballs run --config /path/to/config.json
```

outputs:
```bash
Running. Press CTRL-C to exit.
Web socket server starting on port 6789
```

## To test:
```bash
$ cd tests
$ python test_client.py

```

outputs

```
{"key": "state_of_charge", "unit": "%", "value": 60}
{"key": "charging_current", "unit": "A", "value": 6.0}
{"key": "state_of_charge", "unit": "%", "value": 60}
{"key": "charging_current", "unit": "A", "value": 6.0}
{"key": "state_of_charge", "unit": "%", "value": 60}
{"key": "charging_current", "unit": "A", "value": 6.0}
{"key": "state_of_charge", "unit": "%", "value": 60}
```
