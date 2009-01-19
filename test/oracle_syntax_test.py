import unittest
import oracle_syntax
import pygration


class OracleSyntaxTestCase(unittest.TestCase):
    def setUp( self ):
        self._syntax = oracle_syntax.OracleSyntax()

    def testCreateTableSql( self ):
        columns = [pygration.Number( "id" ), pygration.String("username", 20)]
        sql = self._syntax.create_table_sql( "user", columns )
        expected  = "CREATE TABLE user\n"
        expected += "\t( number id\n"
        expected += "\t, varchar2(20) username\n"
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
                , pygration.String("first_name",32))
        self.assertEqual("ALTER TABLE user ADD varchar2(32) first_name;", sql)

