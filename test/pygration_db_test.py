import unittest
import pygration
import pygration_db
import mock_database


class PygrationDBTestCase(unittest.TestCase):
    def setUp( self ):
        self._db = mock_database.MockDatabase()
        self._pygration_db = pygration_db.PygrationDB( self._db )

    def tearDown( self ):
        self._db = None
        self._pygration_db = None

    def testCreateTable( self ):
        self._pygration_db.create_table( "user", [ \
                pygration.Number( "id" ) ,
                pygration.String( "username", 20 ) ] )
        self.assertEqual( "create table user (number id, string username, )"
                , self._db.last_sql() )

