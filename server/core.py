import asyncio
import functools
from typing import Callable, Optional

from server.helpers import get_current_time
from server.models import Client, Payload
from server.settings import HEARTBEAT_INTERVAL_IN_SECONDS, HEARTBEAT_TIMEOUT_IN_SECONDS


async def heartbeat_daemon(client: Client) -> None:
    """Regularly send `PING` to client while also checking if response (`PONG`) timeout is reached"""
    while not client._closed:
        if (
            get_current_time() - client.last_heartbeat_time
            > HEARTBEAT_TIMEOUT_IN_SECONDS
        ):
            await client.disconnect()
            break
        await client.write("PING")
        await asyncio.sleep(HEARTBEAT_INTERVAL_IN_SECONDS)


def convert_to_payload(data: bytes) -> Optional[Payload]:
    """Convert bytes to a pythonic object to work with"""
    message = data.decode().strip()
    if not message:
        return

    # Ensure every part is a valid string purified from leading and trailing whitespaces
    parts = [part.strip() for part in message.split("|")]
    if any(part == "" for part in parts):
        return None

    message = parts[0].upper()
    args = parts[1:]

    return Payload(message=message, args=args)


def expect_args(n: int):
    """Ensure that the length of `payload.args` is `n`"""

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(client: Client, payload: Payload):
            if len(payload.args) != n:
                return
            return await func(client, payload)

        return wrapper

    return decorator


def expect_a_nick():
    """Ensure that the client has a nickname"""

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(client: Client, payload: Payload):
            if not client.nick:
                await client.write("UNAUTHORIZED")
                return
            return await func(client, payload)

        return wrapper

    return decorator
