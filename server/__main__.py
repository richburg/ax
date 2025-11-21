import asyncio
import logging
from typing import Callable

from server.core.essentials import convert_to_payload, send_heartbeats
from server.core.functions import get_current_time, write_to_all_clients
from server.core.models import Client
from server.handlers.admin import (
    handle_kick,
    handle_mute,
    handle_unmute,
)
from server.handlers.users import handle_auth, handle_list, handle_message, handle_nick
from server.settings import MAX_CLIENT_COUNT, PORT
from server.variables import clients


async def callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    if len(clients) > MAX_CLIENT_COUNT:
        return

    client = Client(get_current_time(), writer, reader)
    clients[writer] = client

    logging.info(f"New connection from {client.ip}")
    heartbeat_task = asyncio.create_task(send_heartbeats(client))

    try:
        while not client._is_closed:
            data = await client.read()
            if not data:
                break

            payload = convert_to_payload(data)
            if not payload:
                continue

            if payload.type_ == "PONG":
                client.last_heartbeat = get_current_time()
                continue

            if client.is_rate_limited():
                logging.warning(f"Too many payloads from {client.ip}")
                await client.write("TOO_MANY_PAYLOADS")
                continue

            mapping: dict[str, Callable] = {
                "NICK": handle_nick,
                "LIST": handle_list,
                "AUTH": handle_auth,
                "KICK": handle_kick,
                "MUTE": handle_mute,
                "UNMUTE": handle_unmute,
                "MESSAGE": handle_message,
            }
            if payload.type_ in mapping:
                await mapping[payload.type_](client, payload)

    except ValueError:
        logging.warning(f"Too large data from {client.ip}")

    except (ConnectionAbortedError, ConnectionResetError, UnicodeDecodeError):
        pass

    except Exception as e:
        logging.error(f"Issues with {client.ip}", exc_info=e)

    finally:
        client = clients.pop(client._writer)
        heartbeat_task.cancel()

        await client.disconnect()

        if client.nickname:
            write_to_all_clients(f"USER_LEAVE|{client.nickname}")

        logging.info(f"Connection closed with {client.ip}")


async def main() -> None:
    server = await asyncio.start_server(callback, "0.0.0.0", PORT, limit=1024)
    logging.info(f"Available on all interfaces at port {PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
