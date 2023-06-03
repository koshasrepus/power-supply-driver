import sys
import asyncio
from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self.command_queue = Queue()
        self.message_queue = Queue()

    def sent_command(self, command: str) -> None:
        self.command_queue.put_nowait(command)

    async def get_command(self):
        return await self.command_queue.get()

    async def sent_message(self, message):
        await self.message_queue.put(message)

    async def get_message(self):
        return await self.message_queue.get()

# class Dispatcher:
#
#     @staticmethod
#     async def get_message() -> str:
#         return await asyncio.to_thread(sys.stdin.readline)
