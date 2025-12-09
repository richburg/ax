from server.core import expect_a_nick, expect_args
from server.helpers import get_client_by_nick, is_valid_nickname, write_to_all_clients
from server.models import Client, Payload


@expect_args(1)
async def handle_nick(client: Client, payload: Payload):
    desired_nick: str = payload.args[0]

    if client.nick:
        await client.write("NICK_ALREADY_SET")
        return

    if not is_valid_nickname(desired_nick):
        await client.write("INVALID_NICK")
        return

    if get_client_by_nick(desired_nick):
        await client.write("NICK_TAKEN")
        return

    client.nick = desired_nick
    await client.write(f"SET_NICK|{desired_nick}")


@expect_a_nick()
@expect_args(1)
async def handle_message(client: Client, payload: Payload):
    message: str = payload.args[0]
    write_to_all_clients(f"NEW_USER_MESSAGE|{client.nick}|{message}")
