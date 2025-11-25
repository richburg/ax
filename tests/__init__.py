import asyncio

HEARTBEAT_TEST_ENABLED: bool = False


class Client:
    def __init__(self) -> None:
        self.reader: asyncio.StreamReader
        self.writer: asyncio.StreamWriter
        self.connected: bool

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection("127.0.0.1", 5000)
        self.connected = True
        return self

    async def __aexit__(self, _, _1, _2):
        self.writer.close()
        await self.writer.wait_closed()

    async def send(self, data: str) -> None:
        self.writer.write((data + "\n").encode())
        await self.writer.drain()

    async def receive(self, duration_in_seconds: int) -> list[str]:
        collected: list[str] = []
        try:
            while True:
                data: bytes = await asyncio.wait_for(
                    self.reader.readline(), timeout=duration_in_seconds
                )
                if not data:
                    self.connected = False
                    break
                collected.append(data.decode().strip())
        except asyncio.TimeoutError:
            pass
        return collected
