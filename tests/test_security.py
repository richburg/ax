import unittest

from server.settings import MAX_PAYLOAD_PER_SECOND

from . import HEARTBEAT_TEST_ENABLED, Client


class TestSecurity(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_nickname(self):
        async with Client() as client:
            await client.send("NICK|!")
            self.assertTrue("NICKNAME_INVALID|!" in await client.receive(1))

    async def test_nickname_not_set(self):
        async with Client() as client:
            await client.send("MESSAGE|hello")
            self.assertTrue("NICKNAME_NOT_SET" in await client.receive(1))

    async def test_nickname_already_in_use(self):
        async with Client() as client:
            await client.send("NICK|hello")
            async with Client() as client:
                await client.send("NICK|hello")
                self.assertTrue(
                    "NICKNAME_ALREADY_IN_USE|hello" in await client.receive(1)
                )

    async def test_big_packets(self):
        async with Client() as client:
            await client.send("x" * 5024)
            await client.receive(1)
            self.assertFalse(client.connected)

    async def test_heartbeat_fail(self):
        if HEARTBEAT_TEST_ENABLED:
            async with Client() as client:
                await client.receive(30)
                self.assertFalse(client.connected)

    async def test_rate_limit(self):
        async with Client() as client:
            for _ in range(MAX_PAYLOAD_PER_SECOND + 1):
                await client.send("data")
            self.assertTrue("TOO_MANY_PAYLOADS" in await client.receive(1))


if __name__ == "__main__":
    unittest.main()
