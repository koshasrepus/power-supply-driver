import asyncio


class ClientPowerSupply:
    def __init__(self, host, port, transport):
        self.host = host
        self.port = port
        self.transport = transport

    @staticmethod
    async def command_process(reader, writer, message):
        message = message + '\n'
        writer.write(message.encode())
        data = await reader.read(100)
        return data.decode('ascii')

    async def run_client(self):
        print('Try connect...')
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888
        )
        print('Connection created!')
        try:
            while True:
                message = await self.transport.get_command()
                result = await self.command_process(reader, writer, message)
                await writer.drain()
                await self.transport.sent_message(result)
        finally:
            writer.close()
            await writer.wait_closed()
