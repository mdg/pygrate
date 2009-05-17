import unittest
import pygrate
import pygrate.pygration
from pygrate.pg_syntax import PgSyntax


class PgSyntaxTestCase(unittest.TestCase):
    def setUp( self ):
        self._syntax = PgSyntax()

    def tearDown(self):
        self._syntax = None

    def testCreateTableSql( self ):
        t = pygrate.Table("user", \
                [pygrate.Number("id")
                ,pygrate.String("username",size=20)
                ])
        sql = self._syntax.create_table_sql(t)
        expected  = "CREATE TABLE user\n"
        expected += "\t( number id\n"
        expected += "\t, varchar(20) username\n"
        expected += "\t);"
        self.assertEqual( expected, sql )

    def testRenameTableSql( self ):
        sql = self._syntax.rename_table_sql( "user", "_hidden_user" )
        self.assertEqual( "ALTER TABLE user RENAME TO _hidden_user;", sql )

    def testDropTableSql( self ):
        sql = self._syntax.drop_table_sql( "_hidden_user" )
        self.assertEqual( "DROP TABLE _hidden_user;", sql )

    def testAddColumnSql( self ):
        sql = self._syntax.add_column_sql("user"
                , pygrate.pygration.String("first_name",32))
        self.assertEqual("ALTER TABLE user ADD varchar(32) first_name;", sql)

