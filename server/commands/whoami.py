from server.core import expect_a_nick, expect_args
from server.models import Client


@expect_a_nick()
@expect_args(0)
async def handle_whoami(client: Client, _):
    """Check your nick"""
    await client.write(f"WHOAMI_OK|{client.nick}")
