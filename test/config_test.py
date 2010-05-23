from unittest import TestCase
from pygration.config import Config, select, UnknownDBError, UnspecifiedDBError


NORMAL_CONFIG_FILE = """
schema: company
connection: oracle://server.com/company
"""

class ConfigTest(TestCase):
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
        self.assertEqual({}, c.opts)


class ConfigSelectTest(TestCase):
    PROD = ['prod.yaml']
    DEV_AND_TEST = ['dev.yaml', 'test.yaml']

    def test_normal_select(self):
        self.assertEquals('dev.yaml', select(self.DEV_AND_TEST, 'dev'))

    def test_select_one_with_none(self):
        self.assertEquals('prod.yaml', select(self.PROD, None))

    def test_select_missing_db_failure(self):
        test = lambda: select(self.DEV_AND_TEST, 'prod')
        self.assertRaises(UnknownDBError, test)

    def test_select_two_with_none_failure(self):
        test = lambda: select(self.DEV_AND_TEST, None)
        self.assertRaises(UnspecifiedDBError, test)
