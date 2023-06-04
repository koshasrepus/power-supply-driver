from asyncio import sleep

from app.commands import BaseChannel
from app.dispatcher import Dispatcher
from app.telemetry_logger import AbstractTelemetryExporter


async def reading_telemetry(dispatcher: Dispatcher, commands: BaseChannel, telemetry_logger: AbstractTelemetryExporter):
    commands_telemetry = list(commands)
    while True:
        for command in commands_telemetry:
            dispatcher.sent_command(command)
            message = await dispatcher.get_message()
            telemetry_logger.export_telemetry(message)
        await sleep(3)
