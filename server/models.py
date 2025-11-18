from asyncio import StreamReader, StreamWriter
from collections import deque
from dataclasses import dataclass
from time import monotonic
from typing import Optional

from server.settings import MAX_PAYLOAD_PER_SECOND


@dataclass
class Client:
    last_heartbeat: float

    _writer: StreamWriter
    _reader: StreamReader
    _is_closed: bool = False
    _timestamps = deque()

    nickname: Optional[str] = None

    async def disconnect(self) -> None:
        """Close the connection"""
        self._writer.close()
        await self._writer.wait_closed()
        self._is_closed = True

    async def write(self, content: str) -> None:
        """Write data to client socket"""
        if not self._is_closed:
            self._writer.write((content + "\n").encode())
            await self._writer.drain()

    async def read(self) -> Optional[bytes]:
        """Read data from client socket until newline"""
        if not self._is_closed:
            data = await self._reader.readline()
            return data

    def is_rate_limited(self) -> bool:
        """Check if the client is currently rate-limited"""
        now = monotonic()

        # Remove all the timestamps older than 1 second
        while self._timestamps and now - self._timestamps[0] > 1:
            self._timestamps.popleft()

        # If there are less timestamps than `MAX_PAYLOAD_PER_SECOND`, mark as __not__ rate-limited
        if len(self._timestamps) < MAX_PAYLOAD_PER_SECOND:
            self._timestamps.append(now)
            return False

        return True

    @property
    def ip(self) -> str:
        """Get IP address of the client"""
        return self._writer.get_extra_info("peername")[0]

    @property
    def admin(self) -> bool:
        """Check if client is admin"""
        if not self.nickname:
            return False
        return self.nickname.startswith("@")


@dataclass
class Payload:
    """Represents a message in the connection flow"""

    type_: str
    args: list[str]
