import pygrate
from pygrate.database import Config
import unittest


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self._config = Config()

    def tearDown(self):
        self._config = None

    def testLoadYamlConf( self ):
        conf = """
schema: app_schema
"""
        self._config._load_yaml_conf(conf)
        self.assertEqual( "app_schema", self._config.schema )

    def testLoadYamlDb(self):
        db = """
driver: pygresql
database: app_db
user: app_user
password: app_pass
"""
        self._config._load_yaml_db(db)
        self.assertEqual('pygresql', self._config.driver)
        self.assertEqual({'driver':'pygresql', 'database':'app_db'
            ,'user':'app_user', 'password':'app_pass'}
            , self._config.db_opts)

