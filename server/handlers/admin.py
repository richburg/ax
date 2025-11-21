from server.core.essentials import expect_admin, expect_args
from server.core.functions import (
    get_client_by_nickname,
)
from server.core.models import Client, Payload


@expect_args(1)
@expect_admin()
async def handle_kick(client: Client, payload: Payload):
    """Disconnect someone from the server"""
    target_nick = payload.args[0]
    target_client = get_client_by_nickname(target_nick)

    if not target_client:
        await client.write("USER_NOT_FOUND")
        return

    if target_client.admin:
        await client.write("USER_IS_ADMIN")
        return

    await target_client.disconnect()


@expect_args(1)
@expect_admin()
async def handle_mute(client: Client, payload: Payload):
    """Mute someone"""
    target_nick = payload.args[0]
    target_client = get_client_by_nickname(target_nick)

    if not target_client:
        await client.write("USER_NOT_FOUND")
        return

    if target_client.admin:
        await client.write("USER_IS_ADMIN")
        return

    target_client.muted = True
    await client.write(f"MUTE_SUCCESS|{target_nick}")


@expect_args(1)
@expect_admin()
async def handle_unmute(client: Client, payload: Payload):
    """Unmute someone"""
    target_nick = payload.args[0]
    target_client = get_client_by_nickname(target_nick)

    if not target_client:
        await client.write("USER_NOT_FOUND")
        return

    target_client.muted = False
    await client.write(f"UNMUTE_SUCCESS|{target_nick}")
