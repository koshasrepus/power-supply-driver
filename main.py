import asyncio

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from worker import Worker
from transport import Dispatcher

from commands import Command, SwitchingPowerChannel
from reading_telemetry import reading_telemetry
from telemetry_logger import FileTelemetryExporter

dispatcher = Dispatcher()
app = FastAPI()


# tasks = BackgroundTasks()
# tasks.add_task(run_worker)

class Channel(BaseModel):
    id: int
    current: str
    voltage: str


@app.post("/channel")
async def create_channel(channel: Channel):
    turn_on_power_channel = SwitchingPowerChannel(channel.id, channel.current, channel.voltage)
    for command in turn_on_power_channel:
        dispatcher.sent_command(command)
    return {"status": 'Ok'}


@app.on_event('startup')
async def driver_connection():
    worker = Worker(dispatcher)
    loop = asyncio.get_event_loop()

    loop.create_task(worker.run_worker())
    loop.create_task(
        reading_telemetry(
            dispatcher,
            Command(root_level='SOURce', channel=1, secondary_level='CURRent'),
            FileTelemetryExporter('export_telemetry.txt')
        )
    )

