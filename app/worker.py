import asyncio


class Worker:
    def __init__(self, host, port, transport):
        self.host = host
        self.port = port
        self.transport = transport

    async def run_worker(self):
        print('Try connect...')
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888
        )
        print('Connection created!')
        while True:
            message = await self.transport.get_command()
            if message == 'close':
                break
            message = message + '\n'
            writer.write(message.encode())
            await writer.drain()
            data = await reader.read(100)
            await self.transport.sent_message(data.decode('ascii'))

        writer.close()
        print('Start close')
        await writer.wait_closed()
        print('End close')


# dispatcher = Worker(Dispatcher())
#
# asyncio.run(dispatcher.run_worker())
