import unittest

from . import Client


class TestMessage(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("MESSAGE|hello, world!")
            self.assertTrue(
                "INCOMING_MESSAGE|test|hello, world!" in await client.receive(0.1)
            )
