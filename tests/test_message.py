import unittest

from . import Client


class TestMessage(unittest.IsolatedAsyncioTestCase):
    async def test_missing_nick(self):
        async with Client() as client:
            await client.send("MESSAGE|hello, world!")
            self.assertTrue("MISSING_NICK" in await client.receive(0.1))

    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("MESSAGE|hello, world!")
            self.assertTrue(
                "NEW_USER_MESSAGE|test|hello, world!" in await client.receive(0.1)
            )
