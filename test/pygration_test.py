import pygration
import unittest


class PygrationColumnTestCase(unittest.TestCase):
    def testString( self ):
        s = pygration.String( "dog" )

        self.assertEqual( "dog", s.name() )
        self.assertEqual( "string", s.type() )

