import pygrate.pygration
import pygrate.pygration_db
import pygrate.oracle_syntax
import mock_database
import unittest


class PygrationDBTestCase(unittest.TestCase):
    def setUp( self ):
        syntax = pygrate.oracle_syntax.OracleSyntax()
        self._conn = mock_database.MockConnection( syntax )
        self._pdb = pygrate.pygration_db.PygrationDB( self._conn )

    def tearDown( self ):
        self._conn = None
        self._pdb = None

    def testCreateTable( self ):
        self._pdb.create_table( "user", [ \
                pygrate.pygration.Number( "id" ) ,
                pygrate.pygration.String( "username", 20 ) ] )
        expected = "CREATE TABLE user\n\t( number id"
        expected += "\n\t, varchar2(20) username\n\t);"
        self.assertEqual( expected, self._conn.last_sql() )

