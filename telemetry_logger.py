import datetime
import json
from abc import ABC, abstractmethod


class AbstractTelemetryExporter(ABC):
    @abstractmethod
    def export_telemetry(self, message):
        pass


class FileTelemetryExporter(AbstractTelemetryExporter):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, file_name):
        self.file_name = file_name
        self.UTC = datetime.timezone.utc

    def export_telemetry(self, message):
        with open(self.file_name, 'a') as f:
            line_to_write = {'time': datetime.datetime.now().strftime(self.TIME_FORMAT), 'data': message}
            json.dump(line_to_write, f)
            f.write('\n')
