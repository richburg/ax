import unittest

from . import Client


class TestAfkSystem(unittest.IsolatedAsyncioTestCase):
    async def test_user_not_found(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("CHECK_AFK|nonexistinguser123")
            self.assertTrue("USER_NOT_FOUND" in await client.receive(0.1))

    async def test(self):
        async with Client() as client:
            await client.send("NICK|test")
            await client.send("TOGGLE_AFK")
            async with Client() as client:
                await client.send("NICK|testtwo")
                await client.send("CHECK_AFK|test")
                self.assertTrue("CHECK_AFK_OK|test|True" in await client.receive(0.1))
