import unittest
import pygration
import pygration_db
import oracle_syntax
import mock_database


class PygrationDBTestCase(unittest.TestCase):
    def setUp( self ):
        syntax = oracle_syntax.OracleSyntax()
        self._conn = mock_database.MockConnection( syntax )
        self._pdb = pygration_db.PygrationDB( self._conn )

    def tearDown( self ):
        self._conn = None
        self._pdb = None

    def testCreateTable( self ):
        self._pdb.create_table( "user", [ \
                pygration.Number( "id" ) ,
                pygration.String( "username", 20 ) ] )
        expected = "CREATE TABLE user\n\t( number id"
        expected += "\n\t, varchar2(20) username\n\t);"
        self.assertEqual( expected, self._conn.last_sql() )

