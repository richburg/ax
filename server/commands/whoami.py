from server.core import expect_a_nick, expect_args
from server.models import Client


@expect_a_nick()
@expect_args(0)
async def handle_whoami(client: Client, _):
    await client.write(f"YOU_ARE|{client.nick}")
