import unittest
import oracle
import pygration


class OracleDatabaseTestCase(unittest.TestCase):
    def setUp( self ):
        self._db = oracle.OracleDatabase()

    def testCreateTableSql( self ):
        columns = [ pygration.Number( "id" ), pygration.String( "username" ) ]
        sql = self._db.create_table_sql( "user", columns )
        expected  = "CREATE TABLE user\n"
        expected += "\t( number id\n"
        expected += "\t, string username\n"
        expected += "\t);"
        self.assertEqual( expected, sql )

