from server.core import expect_args
from server.helpers import get_current_time
from server.models import Client


@expect_args(0)
async def handle_pong(client: Client, _):
    """Refresh `client.last_heartbeat_time`"""
    client.last_heartbeat_time = get_current_time()
