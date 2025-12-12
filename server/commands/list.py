from server.core import expect_a_nick, expect_args
from server.helpers import (
    get_all_nicks,
)
from server.models import Client


@expect_a_nick()
@expect_args(0)
async def handle_list(client: Client, _):
    nicks = get_all_nicks()
    formatted = "|".join(nicks)
    await client.write(f"USER_LIST|{formatted}")
