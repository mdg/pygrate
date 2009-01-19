import pygration
import unittest


class PygrationColumnTestCase(unittest.TestCase):
    def testString( self ):
        s = pygration.String( "dog", 20 )

        self.assertEqual( "dog", s.name() )
        self.assertEqual( "string", s.type() )
        self.assertEqual( "varchar2(20)", s.oracle_type() )

