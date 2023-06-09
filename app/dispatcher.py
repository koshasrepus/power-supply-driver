from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self._command_to_power_supply = Queue()
        self._message_from_power_supply = Queue()

    @staticmethod
    async def _get_data(queue: Queue):
        data = await queue.get()
        queue.task_done()
        return data

    def sent_data(self, command: str) -> None:
        self._command_to_power_supply.put_nowait(command)

    async def get_data(self):
        return await self._get_data(self._command_to_power_supply)

    async def sent_result(self, message):
        await self._message_from_power_supply.put(message)

    async def get_result(self):
        return await self._get_data(self._message_from_power_supply)
