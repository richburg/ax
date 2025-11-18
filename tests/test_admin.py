import random
import unittest

from server.utilities import load_admins

from . import Client


def random_admin_key() -> str:
    all_keys = list(load_admins().keys())
    return random.choice(all_keys)


class TestAdmin(unittest.IsolatedAsyncioTestCase):
    async def test_auth_failure(self):
        async with Client() as client:
            await client.send("AUTH|blabla123")
            self.assertTrue("AUTH_FAILED" in await client.receive(1))

    async def test_auth_success(self):
        async with Client() as client:
            await client.send(f"AUTH|{random_admin_key()}")
            self.assertTrue("AUTH_SUCCESS" in await client.receive(1))


if __name__ == "__main__":
    unittest.main()
