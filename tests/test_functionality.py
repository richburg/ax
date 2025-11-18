import unittest

from . import Client


class TestFunctionality(unittest.IsolatedAsyncioTestCase):
    async def test_nickname(self):
        async with Client() as client:
            await client.send("NICK|john")
            self.assertTrue("USER_JOIN|john" in await client.receive(1))

    async def test_messages(self):
        async with Client() as client:
            await client.send("NICK|john")
            await client.send("MESSAGE|hello, world!")
            self.assertTrue(
                "INCOMING_MESSAGE|john|hello, world!" in await client.receive(1)
            )

    async def test_list(self):
        async with Client() as client:
            await client.send("NICK|john")
            await client.send("LIST")
            self.assertTrue("USER_LIST|john" in await client.receive(1))


if __name__ == "__main__":
    unittest.main()
