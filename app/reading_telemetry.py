from asyncio import sleep

from app.commands import BaseChannel
from app.dispatcher import Dispatcher
from app.telemetry_logger import AbstractTelemetryExporter


async def reading_telemetry(
    dispatcher: Dispatcher, commands: BaseChannel, telemetry_logger: AbstractTelemetryExporter, delay: int
):
    commands_telemetry = list(commands)
    prefix = ''
    while True:
        for command in commands_telemetry:
            dispatcher.sent_data(command)
            message = await dispatcher.get_result()
            if 'MEASure1' in command:
                prefix = 'ch1: '
            elif 'MEASure2' in command:
                prefix = 'ch2: '
            elif 'MEASure3' in command:
                prefix = 'ch3: '
            elif 'MEASure4' in command:
                prefix = 'ch4: '
            message = prefix + message
            telemetry_logger.export_telemetry(message)
            prefix = ''
        await sleep(delay)
