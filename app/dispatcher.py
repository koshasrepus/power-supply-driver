from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self.command_to_power_supply = Queue()
        self.message_from_power_supply = Queue()

    @staticmethod
    async def get_data(queue: Queue):
        data = await queue.get()
        queue.task_done()
        return data

    def sent_command(self, command: str) -> None:
        self.command_to_power_supply.put_nowait(command)

    async def get_command(self):
        return await self.get_data(self.command_to_power_supply)

    async def sent_message(self, message):
        await self.message_from_power_supply.put(message)

    async def get_message(self):
        return await self.get_data(self.message_from_power_supply)
