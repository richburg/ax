from typing import Callable

from server.commands.pong import handle_pong

from .list import handle_list
from .message import handle_message
from .nick import handle_nick
from .whoami import handle_whoami

mapping: dict[str, Callable] = {
    "NICK": handle_nick,
    "LIST": handle_list,
    "MESSAGE": handle_message,
    "WHOAMI": handle_whoami,
    "PONG": handle_pong,
}
