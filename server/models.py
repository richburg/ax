import time
from asyncio import StreamReader, StreamWriter
from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional

from server.settings import MAX_BYTES_PER_SECOND


@dataclass
class Client:
    last_heartbeat_time: float

    _writer: StreamWriter
    _reader: StreamReader

    _closed: bool = False
    _timestamps: deque = field(default_factory=deque)

    nick: Optional[str] = None  # Min: 2 Max: 12
    away: bool = False

    @cached_property
    def ip(self) -> str:
        return self._writer.get_extra_info("peername")[0]

    @property
    def rate_limited(self) -> bool:
        now = time.monotonic()

        # Clears timestamps older than 1 second
        while self._timestamps and now - self._timestamps[0] >= 1:
            self._timestamps.popleft()

        # Check if rate limited
        if len(self._timestamps) >= MAX_BYTES_PER_SECOND:
            return True

        # New payload sent -> new timestamp
        self._timestamps.append(now)
        return False

    async def write(self, content: str) -> None:
        """Write data to client socket"""
        if self._closed:
            return
        try:
            self._writer.write((content + "\n").encode())
            await self._writer.drain()
        except OSError:
            self._closed = True

    async def read(self) -> Optional[bytes]:
        """Read data from client socket until newline"""
        try:
            if not self._closed:
                return await self._reader.readline()
        except OSError:
            self._closed = True

    async def disconnect(self) -> None:
        """Close the connection safely"""
        self._writer.close()
        if not self._closed:
            try:
                await self._writer.wait_closed()
            except OSError:
                pass
            self._closed = True

    def __str__(self) -> str:
        return f"{self.ip}:{self.nick or 'None'}"


@dataclass
class Payload:
    """Represents a message in the connection flow"""

    message: str
    args: list[str]
