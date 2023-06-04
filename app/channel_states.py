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
        with open(self.file_name, 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode().strip()
            return last_line


def channel_states(states_reader: AbstractChannelStates = None):
    states_reader = states_reader or FileChannelStates(config.telemetry_export_file)
    result = states_reader.states()
    return result
