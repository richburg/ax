from server.core import expect_a_nick, expect_args
from server.helpers import (
    write_to_all_clients,
)
from server.models import Client, Payload


@expect_a_nick()
@expect_args(1)
async def handle_message(client: Client, payload: Payload):
    message = payload.args[0]
    write_to_all_clients(f"NEW_USER_MESSAGE|{client.nick}|{message}")
