import json
from asyncio import sleep

from transport import Dispatcher
from commands import Command


async def reading_telemetry(dispatcher: Dispatcher, command: Command):
    command = command.json()
    command = json.loads(command)['command']
    while True:
        dispatcher.sent_command(command)
        await sleep(3)

