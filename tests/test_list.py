import unittest

from . import Client


class TestList(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("LIST")
            self.assertTrue("LIST_OK|test" in await client.receive(0.1))
