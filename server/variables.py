from asyncio import StreamWriter

from server.models import Client

clients: dict[StreamWriter, Client] = {}
