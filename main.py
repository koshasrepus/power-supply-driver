import asyncio

from fastapi import FastAPI

from app.channel_states import channel_states
from app.client import ClientPowerSupply
from app.commands import (OffChannel, ReadTelemetryChannel,
                          SwitchingPowerChannel)
from app.config import config
from app.dispatcher import Dispatcher
from app.query_body_models import TurnOffChannel, TurnOnChannel
from app.reading_telemetry import reading_telemetry
from app.telemetry_logger import FileTelemetryExporter

dispatcher = Dispatcher()
app = FastAPI()


@app.post("/channel")
async def create_channel(channel: TurnOnChannel):
    turn_on_power_channel = SwitchingPowerChannel(channel.id, channel.current, channel.voltage)
    for command in turn_on_power_channel:
        dispatcher.sent_command(command)
        result = await dispatcher.get_message()
        print(result)
    return {"status": 'Ok'}


@app.get('/channel')
async def get_channel_states():
    data = channel_states()
    return {"data": data}


@app.patch('/channel')
async def off_channel(channel: TurnOffChannel):
    off_channel_command = OffChannel(channel.id)
    dispatcher.sent_command(next(off_channel_command))
    result = await dispatcher.get_message()
    print(result)
    return {"status": 'Ok'}


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
