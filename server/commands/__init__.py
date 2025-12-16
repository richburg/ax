from typing import Callable

from .afk import handle_check_afk, handle_toggle_afk
from .list import handle_list
from .message import handle_message
from .nick import handle_nick
from .whoami import handle_whoami

mapping: dict[str, Callable] = {
    "NICK": handle_nick,
    "LIST": handle_list,
    "MESSAGE": handle_message,
    "WHOAMI": handle_whoami,
    "TOGGLE_AFK": handle_toggle_afk,
    "CHECK_AFK": handle_check_afk,
}
