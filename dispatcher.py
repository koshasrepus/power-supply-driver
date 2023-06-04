import sys
import asyncio
from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self.command_queue = Queue()
        self.message_queue = Queue()

    @staticmethod
    async def get_data(queue: Queue):
        data = await queue.get()
        queue.task_done()
        return data

    def sent_command(self, command: str) -> None:
        self.command_queue.put_nowait(command)

    async def get_command(self):
        return await self.get_data(self.command_queue)

    async def sent_message(self, message):
        await self.message_queue.put(message)

    async def get_message(self):
        return await self.get_data(self.message_queue)

