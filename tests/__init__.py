import asyncio
import logging

from server.settings import HOST, PORT

HEARTBEAT_TEST_ENABLED = False


class Client:
    def __init__(self) -> None:
        self.reader: asyncio.StreamReader
        self.writer: asyncio.StreamWriter
        self.connected: bool = False

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        self.connected = True
        return self

    async def __aexit__(self, _, _1, _2):
        self.writer.close()
        await self.writer.wait_closed()
        self.connected = False

    async def send(self, message: str) -> None:
        self.writer.write((message + "\n").encode())
        await self.writer.drain()

    async def receive(self, duration: float) -> list[str]:
        collected = []
        try:
            async with asyncio.timeout(duration):
                while self.connected:
                    data: bytes = await self.reader.readline()
                    if not data:
                        self.connected = False
                    message: str = data.decode().strip()
                    collected.append(message)
        except TimeoutError:
            pass
        except Exception as e:
            logging.error("Something went wrong when testing", exc_info=e)
        return collected
