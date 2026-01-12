import asyncio
import re
from typing import Optional

from server.models import Client
from server.variables import clients


def get_current_time():
    """Return the current runng loop time in UNIX timestamp format"""
    return asyncio.get_running_loop().time()


def broadcast(content: str):
    """Write `content` to all clients"""
    for client in clients:
        asyncio.create_task(client.write(content))


def register_new_client(
    writer: asyncio.StreamWriter, reader: asyncio.StreamReader
) -> Client:
    """In-memory registration"""
    client = Client(get_current_time(), writer, reader)
    clients.append(client)
    return client


def get_client_by_nick(nick: str) -> Optional[Client]:
    """Get a client by its nickanme"""
    return next((client for client in clients if client.nick == nick), None)


def is_valid_nick(nickname: str) -> bool:
    """Only **lowercase** letters and between **1-12** characters long."""
    regex_for_a_valid_nickname = r"^[a-z]{1,12}$"
    return bool(re.fullmatch(regex_for_a_valid_nickname, nickname))
