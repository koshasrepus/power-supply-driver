import sys
import asyncio
from asyncio import Queue


class Dispatcher:
    def __init__(self):
        self.queue = Queue()

    def sent_command(self, command: str) -> None:
        self.queue.put_nowait(command)

    async def get_message(self):
        return await self.queue.get()

# class Dispatcher:
#
#     @staticmethod
#     async def get_message() -> str:
#         return await asyncio.to_thread(sys.stdin.readline)
