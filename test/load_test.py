import unittest
from pygration.load import Config


NORMAL_CONFIG_FILE = """
schema: company
connection: oracle://server.com/company
"""

class ConfigTest(unittest.TestCase):
    """Test the Config object and how it loads options."""

    def test_normal_config(self):
        c = Config()
        c.load(NORMAL_CONFIG_FILE)

        self.assertEqual('company', c.schema)
        self.assertEqual('oracle://server.com/company', c.connection)

    def test_empty_config(self):
        c = Config()
        c.load('')

        self.assertEqual(None, c.schema)
        self.assertEqual(None, c.connection)
        self.assertEqual({}, c.db_opts)

