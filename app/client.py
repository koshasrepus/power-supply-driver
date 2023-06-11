import asyncio


class ClientPowerSupply:
    def __init__(self, host, port, transport):
        self.host = host
        self.port = port
        self.transport = transport

    @staticmethod
    async def sending_data(reader, writer, message):
        message = message + '\n'
        writer.write(message.encode())
        data = await reader.read(100)
        return data.decode('ascii')

    async def run_client(self):
        print('Try connect...')
        reader, writer = await asyncio.open_connection(
            self.host, self.port
        )
        print('Connection created!')
        try:
            while True:
                data = await self.transport.get_data()
                result = await self.sending_data(reader, writer, data)
                await writer.drain()
                await self.transport.sent_result(result)
        finally:
            writer.close()
            await writer.wait_closed()
