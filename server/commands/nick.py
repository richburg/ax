from server.core import expect_args
from server.helpers import (
    get_client_by_nick,
    is_valid_nick,
)
from server.models import Client, Payload


@expect_args(1)
async def handle_nick(client: Client, payload: Payload):
    """Set a nick"""
    desired_nick = payload.args[0]

    if client.nick:
        await client.write("NICK_ALREADY_SET")
        return

    if not is_valid_nick(desired_nick):
        await client.write("NICK_INVALID")
        return

    if get_client_by_nick(desired_nick):
        await client.write("NICK_TAKEN")
        return

    client.nick = desired_nick
    await client.write(f"NICK_OK|{desired_nick}")
