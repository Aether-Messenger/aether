import unittest

import app.core.security as security


class SecurityTests(unittest.TestCase):
    def test_hash_password(self):
        password = "password"

        hash1 = security.hash_password(password)
        hash2 = security.hash_password(password)

        self.assertNotEqual(hash1, password)
        self.assertNotEqual(hash1, hash2)
        self.assertTrue(hash1.startswith("$argon2id$"))

    def test_verify_password(self):
        password = "password"
        hashed = security.hash_password(password)

        self.assertTrue(security.verify_password(password, hashed))
        self.assertFalse(security.verify_password("wrong", hashed))


if __name__ == "__main__":
    unittest.main()
