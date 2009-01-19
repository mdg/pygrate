import pygrate.pygration
import unittest


class PygrationColumnTestCase(unittest.TestCase):
    def testString( self ):
        s = pygrate.pygration.String( "dog", 20 )

        self.assertEqual( "dog", s.name() )
        self.assertEqual( "string", s.type() )
        self.assertEqual( "varchar2(20)", s.oracle_type() )

