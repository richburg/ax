from server.core import expect_a_nick, expect_args
from server.helpers import get_client_by_nick
from server.models import Client, Payload


@expect_a_nick()
@expect_args(0)
async def handle_toggle_afk(client: Client, _):
    """Toggle your AFK status"""
    client.away = not client.away
    await client.write("TOGGLE_AFK_OK")


@expect_a_nick()
@expect_args(1)
async def handle_check_afk(client: Client, payload: Payload):
    """Check if someone is AFK"""
    target_nick = payload.args[0]
    target = get_client_by_nick(target_nick)

    if not target:
        await client.write("USER_NOT_FOUND")
        return

    await client.write(f"CHECK_AFK_OK|{target_nick}|{target.away}")
