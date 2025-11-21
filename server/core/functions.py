import asyncio
import re
from typing import Optional

from server.core.models import Client
from server.variables import clients


def get_current_time():
    """Return the current runng loop time in UNIX timestamp format"""
    return asyncio.get_running_loop().time()


def get_client_by_nickname(nickname: str) -> Optional[Client]:
    """Get a client by its nickname"""
    return next(
        (client for client in clients.values() if client.nickname == nickname), None
    )


def get_all_nicknames() -> list[str]:
    """Query all the registered nicknames"""
    return [client.nickname or "" for client in clients.values()]


def is_valid_nickname(nickname: str) -> bool:
    """Only **lowercase** letters and between **1-12** characters long."""
    regex_for_a_valid_nickname = r"^[a-z]{1,12}$"
    return bool(re.fullmatch(regex_for_a_valid_nickname, nickname))


def write_to_all_clients(content: str):
    """Write `content` to all clients"""
    for client in clients.values():
        asyncio.create_task(client.write(content))


def load_admins() -> dict[str, str]:
    """Parse administrator accounts along with their nickname and key from `admins.conf`"""
    result = {}
    with open("admins.conf", "r") as file:
        for line in file.readlines():
            try:
                key, nick = line.split(":")
                result[key] = nick
            except ValueError:
                raise Exception("Configuration file is corrupted")
    return result
