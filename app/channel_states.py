import json
import os
from abc import ABC, abstractmethod

from app.config import config


class AbstractChannelStates(ABC):
    @abstractmethod
    def states(self):
        pass


class FileChannelStates(AbstractChannelStates):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def states(self):
        log_data = []
        with open(self.file_name, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while len(log_data) < 4:
                    current_character = f.read(1)
                    line = []
                    while current_character != b'\n':
                        line.append(current_character.decode('ascii'))
                        f.seek(-2, os.SEEK_CUR)
                        current_character = f.read(1)
                    cur_line = ''.join(line[::-1])
                    log_data.append(
                        json.loads(cur_line)
                    )
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            return log_data


def channel_states(states_reader: AbstractChannelStates = None):
    states_reader = states_reader or FileChannelStates(config.telemetry_export_file)
    result = states_reader.states()
    return result
