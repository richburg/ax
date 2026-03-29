import time
from asyncio import StreamReader, StreamWriter
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

from server.settings import MAX_REQUESTS_PER_SECOND


@dataclass
class Client:
    last_heartbeat_time: float

    _writer: StreamWriter
    _reader: StreamReader

    _closed: bool = False

    _last_refill: float = field(default_factory=time.monotonic)
    _tokens: float = field(default=MAX_REQUESTS_PER_SECOND)

    nick: Optional[str] = None

    @cached_property
    def ip(self) -> str:
        """Cached IP address"""
        return self._writer.get_extra_info("peername")[0]

    def is_rate_limited(self) -> bool:
        """Implements the token bucket algorithm"""
        now = time.monotonic()
        elapsed = now - self._last_refill

        how_many_tokens_to_add: float = elapsed * MAX_REQUESTS_PER_SECOND
        self._tokens = min(
            MAX_REQUESTS_PER_SECOND, self._tokens + how_many_tokens_to_add
        )
        self._last_refill = now

        if self._tokens < 1:
            return True

        self._tokens -= 1
        return False

    async def write(self, content: str) -> None:
        """Write data to client socket"""
        if self._closed:
            return
        try:
            self._writer.write((content + "\n").encode())
            await self._writer.drain()
        except (OSError, ConnectionError):
            self._closed = True

    async def read(self) -> Optional[bytes]:
        """Read data from client socket until newline"""
        if self._closed:
            return
        try:
            received = await self._reader.readline()
            return received
        except (OSError, ConnectionError):
            self._closed = True

    async def disconnect(self) -> None:
        """Close the connection safely"""
        self._writer.close()
        try:
            await self._writer.wait_closed()
        except (OSError, ConnectionError):
            pass
        self._closed = True

    def __str__(self) -> str:
        if self.nick and self.ip:
            return self.ip + ":" + self.nick
        return self.ip


@dataclass
class Payload:
    """Represents a payload from client"""

    message: str
    args: list[str]
