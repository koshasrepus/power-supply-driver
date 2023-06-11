import json
import os
from abc import ABC, abstractmethod

from config import config


class AbstractTelemetryExtract(ABC):
    @abstractmethod
    def states(self):
        pass


class FileTelemetryExtract(AbstractTelemetryExtract):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def states(self):
        """Возвращает последние 4 строки из файла"""
        log_data = []
        seek_step = -2
        with open(self.file_name, 'rb') as f:
            try:
                f.seek(seek_step, os.SEEK_END)
                while len(log_data) < 4:
                    current_character = f.read(1)
                    line = []
                    while current_character != b'\n' and f.tell():
                        line.append(current_character.decode('ascii'))
                        if f.tell() == 1:
                            seek_step = -1
                        f.seek(seek_step, os.SEEK_CUR)
                        current_character = f.read(1)
                        if seek_step == -1:
                            break
                    cur_line = ''.join(line[::-1])
                    log_data.append(
                        json.loads(cur_line)
                    )
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            return log_data


def get_channel_states(states_reader: AbstractTelemetryExtract = None):
    states_reader = states_reader or FileTelemetryExtract(config.telemetry_export_file)
    result = states_reader.states()
    return result
