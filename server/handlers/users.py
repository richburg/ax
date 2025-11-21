from server.core.essentials import expect_args, expect_nick
from server.core.functions import (
    get_all_nicknames,
    get_client_by_nickname,
    is_valid_nickname,
    load_admins,
    write_to_all_clients,
)
from server.core.models import Client, Payload


@expect_args(1)
async def handle_nick(client: Client, payload: Payload):
    """Set a nickname"""
    desired_nickname: str = payload.args[0]

    if client.nickname:
        await client.write("NICKNAME_ALREADY_SET")
        return

    if not is_valid_nickname(desired_nickname):
        await client.write(f"NICKNAME_INVALID|{desired_nickname}")
        return

    if get_client_by_nickname(desired_nickname):
        await client.write(f"NICKNAME_ALREADY_IN_USE|{desired_nickname}")
        return

    client.nickname = desired_nickname
    write_to_all_clients(f"USER_JOIN|{desired_nickname}")


@expect_args(1)
@expect_nick()
async def handle_message(client: Client, payload: Payload):
    """Send a message"""
    if client.muted:
        return
    message: str = payload.args[0]
    write_to_all_clients(f"INCOMING_MESSAGE|{client.nickname}|{message}")


@expect_nick()
async def handle_list(client: Client, _):
    """Get a list of all clients"""
    formatted_client_details = "|".join(get_all_nicknames())
    await client.write(f"USER_LIST|{formatted_client_details}")


@expect_args(1)
async def handle_auth(client: Client, payload: Payload):
    """Authenticate as admin"""
    admin_keys = load_admins()
    key: str = payload.args[0]

    if key not in admin_keys:
        await client.write("AUTH_FAILED")
        return

    client.nickname = "@" + admin_keys[key]
    await client.write("AUTH_SUCCESS")
