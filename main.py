import asyncio

from fastapi import FastAPI

from app.channel_states import get_channel_states
from app.client import ClientPowerSupply
from app.commands import (
    OffChannel,
    ReadTelemetryChannel,
    SwitchingPowerChannel,
)
from app.dispatcher import Dispatcher
from app.query_body_models import TurnOffChannel, TurnOnChannel
from app.reading_telemetry import reading_telemetry
from app.telemetry_logger import FileTelemetryExporter
from config import config

dispatcher = Dispatcher()
app = FastAPI()


@app.post("/channel")
async def turn_on_channel(channel: TurnOnChannel):
    turn_on_power_channel = SwitchingPowerChannel(channel.id, channel.current, channel.volt)
    for command in turn_on_power_channel:
        dispatcher.sent_data(command)
        result = await dispatcher.get_result()
        print(result)
    return {"status": 'Ok'}


@app.patch('/channel')
async def turn_off_channel(channel: TurnOffChannel):
    off_channel_command = OffChannel(channel.id)
    dispatcher.sent_data(next(off_channel_command))
    result = await dispatcher.get_result()
    print(result)
    return {"status": 'Ok'}


@app.get('/channel')
async def channel_states():
    data = get_channel_states()
    return {"data": data}


@app.on_event('startup')
def driver_connection():
    client_power_supply = ClientPowerSupply(config.power_supply_host, config.power_supply_port, dispatcher)
    asyncio.create_task(client_power_supply.run_client())
    asyncio.create_task(
        reading_telemetry(
            dispatcher,
            ReadTelemetryChannel(),
            FileTelemetryExporter(config.telemetry_export_file),
            config.telemetry_delay
        )
    )
