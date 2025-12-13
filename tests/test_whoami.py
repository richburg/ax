import unittest

from . import Client


class TestWhoami(unittest.IsolatedAsyncioTestCase):
    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("WHOAMI")
            self.assertTrue("WHOAMI_OK|test" in await client.receive(0.1))
