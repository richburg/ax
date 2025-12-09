import unittest

from server.settings import HEARTBEAT_TIMEOUT_IN_SECONDS, MAX_BYTES_PER_SECOND

from . import HEARTBEAT_TEST_ENABLED, Client


class TestSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_big_packets(self):
        async with Client() as client:
            await client.send("x" * 2048)
            await client.receive(0.1)
            self.assertFalse(client.connected)

    async def test_flooding(self):
        async with Client() as client:
            for _ in range(MAX_BYTES_PER_SECOND + 1):
                await client.send("x")
            self.assertTrue("SLOW_DOWN" in await client.receive(0.1))

    async def test_heartbeat_logic(self):
        if HEARTBEAT_TEST_ENABLED:
            async with Client() as client:
                await client.receive(HEARTBEAT_TIMEOUT_IN_SECONDS)
                self.assertFalse(client.connected)
