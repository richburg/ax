import asyncio
import functools
import logging
from typing import Callable, Optional

from server.models import Client, Payload
from server.settings import HEARTBEAT_INTERVAL_IN_SECONDS, HEARTBEAT_TIMEOUT_IN_SECONDS
from server.utilities import get_current_time


async def send_heartbeats(client: Client) -> None:
    """Regularly send `PING` to client while also checking if response (`PONG`) timeout is reached"""
    while not client._is_closed:
        if get_current_time() - client.last_heartbeat > HEARTBEAT_TIMEOUT_IN_SECONDS:
            await client.disconnect()
            break
        try:
            await client.write("PING")
            await asyncio.sleep(HEARTBEAT_INTERVAL_IN_SECONDS)
        except Exception as e:
            logging.error(f"Failed to send heartbeat to {client.ip}: {e}")
            await client.disconnect()
            break


def convert_to_payload(data: bytes) -> Optional[Payload]:
    """Convert bytes to a pythonic object to work with"""
    message: str = data.decode().strip()  # Decode and remove whitespaces
    if not message:
        return None

    # Split (separator is "|") into so called `parts`
    parts: list[str] = message.split("|")
    if not parts:
        return None

    type_: str = parts[0].upper()
    args: list[str] = parts[1:] if len(parts) >= 2 else []  # No arguments = `None`

    return Payload(type_=type_, args=args)


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


def expect_nick():
    """Ensure that the client has a nickname"""

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(client: Client, payload: Payload):
            if not client.nickname:
                await client.write("NICKNAME_NOT_SET")
                return
            return await func(client, payload)

        return wrapper

    return decorator
