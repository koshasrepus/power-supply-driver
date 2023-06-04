import os
import asyncio

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from worker import Worker
from dispatcher import Dispatcher

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
    return 201, {"status": 'Ok'}


@app.get('/channel')
async def get_channel_states():
    with open('export_telemetry.txt', 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode().strip()
    return {"data": last_line}


@app.on_event('startup')
def driver_connection():
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

