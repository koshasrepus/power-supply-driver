import json
from asyncio import sleep

from transport import Dispatcher
from commands import Command
from telemetry_logger import AbstractTelemetryExporter


async def reading_telemetry(dispatcher: Dispatcher, command: Command, telemetry_logger: AbstractTelemetryExporter):
    command = command.json()
    command = json.loads(command)['command']
    while True:
        dispatcher.sent_command(command)
        message = await dispatcher.get_message()
        telemetry_logger.export_telemetry(message)
        await sleep(3)
