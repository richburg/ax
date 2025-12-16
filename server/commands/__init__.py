from typing import Callable

from .afk_system import handle_status, handle_toggleafk
from .list import handle_list
from .message import handle_message
from .nick import handle_nick
from .whoami import handle_whoami

mapping: dict[str, Callable] = {
    "NICK": handle_nick,
    "LIST": handle_list,
    "MESSAGE": handle_message,
    "WHOAMI": handle_whoami,
    "TOGGLEAFK": handle_toggleafk,
    "STATUS": handle_status,
}
