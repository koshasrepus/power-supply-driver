from collections import deque


class Command:
    def __init__(self, *args, channel=None, parameters=None):
        self.keywords = f':{args[0]}{channel or ""}:' + ':'.join(args[1:])
        self.parameters = '?' if not parameters else (' ' + parameters)

    def __str__(self):
        return self.keywords + self.parameters


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
        set_current = Command('SOURce', 'CURRent', channel=channel_id,  parameters=current)
        set_voltage = Command('SOURce', 'VOLTage', channel=channel_id, parameters=voltage)
        turn_power_channel = Command('OUTPUT', 'STATe', channel=channel_id, parameters='ON')
        for command in (set_current, set_voltage, turn_power_channel):
            self.commands.append(str(command))


class OffChannel(BaseChannel):
    def __init__(self, channel_id: int):
        super(OffChannel, self).__init__()
        self.init_commands(channel_id)

    def init_commands(self, channel_id: int):
        command = Command('OUTPut', 'STATe',  channel=channel_id, parameters='OFF')
        self.commands.append(str(command))


class ReadTelemetryChannel(BaseChannel):
    def __init__(self):
        super(ReadTelemetryChannel, self).__init__()
        self.init_commands()

    def init_commands(self):
        for channel in range(1, 4 + 1):
            self.commands.append(
                str(
                    Command('MEASure', 'ALL',  channel=channel)
                )
            )
