import json
from typing import Literal, Any
from pydantic import BaseModel
import json
import queue


def json_dumps(v, *, default):
    result = {
        'command': f':{v["root_level"]}{v["channel"]}:{v["secondary_level"]}' +
                   (f':{v["tertiary_level"]}' if v["tertiary_level"] else '') +
                   ('' if v["parameters"] == '?' else ' ' + v["parameters"])
    }
    return json.dumps(result)


class Command(BaseModel):
    root_level: Literal['SOURce', 'OUTPut', 'OUTPUT']
    channel: Literal[1, 2, 3, 4]
    secondary_level: Literal['CURRent', 'VOLTage', 'STATe']
    tertiary_level: Literal['ENABle'] = None
    parameters: str = '?'

    class Config:
        json_dumps = json_dumps
        dict = json_dumps


class SwitchingPowerChannel:
    def __init__(self, id: int, current: str, voltage: str):
        self.commands = queue.Queue()
        self.init_commands(id, current, voltage)

    def __iter__(self):
        return self

    def __next__(self):
        while not self.commands.empty():
            return self.commands.get()
        raise StopIteration()

    def init_commands(self, id: int, current: str, voltage: str):
        set_current = Command(root_level='SOURce', channel=id, secondary_level='CURRent', parameters=current)
        set_voltage = Command(root_level='SOURce', channel=id, secondary_level='VOLTage', parameters=voltage)
        turn_power_channel = Command(root_level='OUTPUT', channel=id, secondary_level='STATe', parameters='ON')
        for command in (set_current, set_voltage, turn_power_channel):
            command = command.json(models_as_dict=True)
            command = json.loads(command)['command']
            self.commands.put(command)

