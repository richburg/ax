import unittest

from . import Client


class TestNick(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_nick(self):
        async with Client() as client:
            await client.send(f"NICK|{'x' * 13 + '!?.-'}")
            self.assertTrue("NICK_INVALID" in await client.receive(0.1))

    async def test_nick_duplicate(self):
        async with Client() as client:
            await client.send("NICK|test")
            async with Client() as client:
                await client.send("NICK|test")
                self.assertTrue("NICK_TAKEN" in await client.receive(0.1))

    async def test_already_set_nick(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("NICK|test")
            self.assertTrue("NICK_ALREADY_SET" in await client.receive(0.1))

    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            self.assertTrue("NICK_OK|test" in await client.receive(0.1))
