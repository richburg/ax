from server.core import expect_a_nick, expect_args
from server.models import Client
from server.variables import clients


@expect_a_nick()
@expect_args(0)
async def handle_list(client: Client, _):
    """Get a list of all the users"""
    all_the_nicks: list[str] = [client.nick or "" for client in clients]
    formatted_response = "|".join(all_the_nicks)
    await client.write(f"LIST_OK|{formatted_response}")
