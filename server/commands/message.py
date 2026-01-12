from server.core import expect_a_nick, expect_args
from server.helpers import broadcast
from server.models import Client, Payload


@expect_a_nick()
@expect_args(1)
async def handle_message(client: Client, payload: Payload):
    """Send a new message"""
    message = payload.args[0]
    broadcast(f"INCOMING_MESSAGE|{client.nick}|{message}")
