from asyncio import StreamWriter

from server.core.models import Client

clients: dict[StreamWriter, Client] = {}
