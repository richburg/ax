import asyncio
import logging

from server.commands import mapping
from server.core import convert_to_payload, heartbeat_daemon
from server.helpers import broadcast, get_current_time, register_new_client
from server.settings import HOST, MAX_CLIENT_COUNT, PORT
from server.variables import clients


async def callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    if len(clients) > MAX_CLIENT_COUNT:
        return

    client = register_new_client(writer, reader)
    logging.info(f"New connection from {client}")

    heartbeat_task = asyncio.create_task(heartbeat_daemon(client))

    try:
        while not client._closed:
            data = await client.read()
            if not data:
                break

            if client.rate_limited:
                logging.warning(f"Slowed down {client}")
                await client.write("SLOW_DOWN")
                continue

            payload = convert_to_payload(data)
            if not payload:
                continue

            if payload.message == "PONG":
                client.last_heartbeat_time = get_current_time()
                continue

            if payload.message in mapping:
                await mapping[payload.message](client, payload)

    except UnicodeDecodeError:
        logging.warning(f"Invalid data from {client}")

    except ValueError:
        logging.warning(f"Too large data from {client}")

    except Exception as e:
        logging.error(client, exc_info=e)

    finally:
        await client.disconnect()

        clients.remove(client)
        heartbeat_task.cancel()

        if client.nick:
            broadcast(f"LEFT|{client.nick}")

        logging.info(f"Connection closed with {client}")


async def main() -> None:
    server = await asyncio.start_server(callback, HOST, PORT, limit=1024)
    logging.info(f"Available on all interfaces at port {PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
