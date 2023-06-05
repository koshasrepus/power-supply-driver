from collections import deque


class Command:
    def __init__(self, root_level, channel, secondary_level, *, tertiary_level=None, parameters=None):
        self.root_level = root_level
        self.channel = channel
        self.secondary_level = secondary_level
        self.tertiary_level = (':' + tertiary_level) if tertiary_level else ''
        self.parameters = '?' if not parameters else (' ' + parameters)

    def __str__(self):
        return f':{self.root_level}{self.channel}:' \
               f'{self.secondary_level}{self.tertiary_level}{self.parameters}'


class BaseChannel:
    def __init__(self):
        self.commands = deque()

    def __iter__(self):
        return self

    def __next__(self):
        while self.commands:
            return self.commands.popleft()
        raise StopIteration()


class SwitchingPowerChannel(BaseChannel):
    def __init__(self, channel_id: int, current: str, voltage: str):
        super(SwitchingPowerChannel, self).__init__()
        self.init_commands(channel_id, current, voltage)

    def init_commands(self, channel_id: int, current: str, voltage: str):
        set_current = Command('SOURce', channel_id, 'CURRent', parameters=current)
        set_voltage = Command('SOURce', channel_id, 'VOLTage', parameters=voltage)
        turn_power_channel = Command('OUTPUT', channel_id, 'STATe', parameters='ON')
        for command in (set_current, set_voltage, turn_power_channel):
            self.commands.append(str(command))


class OffChannel(BaseChannel):
    def __init__(self, channel_id: int):
        super(OffChannel, self).__init__()
        self.init_commands(channel_id)

    def init_commands(self, channel_id: int):
        command = Command('OUTPut', channel_id, 'STATe', parameters='OFF')
        self.commands.append(str(command))


class ReadTelemetryChannel(BaseChannel):
    def __init__(self):
        super(ReadTelemetryChannel, self).__init__()
        self.init_commands()

    def init_commands(self):
        for command in (('MEASure', channel_id, 'ALL') for channel_id in range(1, 4 + 1)):
            self.commands.append(str(Command(*command)))
