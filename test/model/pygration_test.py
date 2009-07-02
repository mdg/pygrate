import pygrate
from pygrate import pygration
from pygrate.pygration import PygrationType
from pygrate.pygrator import Pygrator
import unittest


class PygrationColumnTestCase(unittest.TestCase):
    def testString( self ):
        s = pygrate.String( "dog", 20 )

        self.assertEqual( "dog", s.name() )
        self.assertEqual( "string", s.type() )
        self.assertEqual( "varchar2(20)", s.oracle_type() )

class PygrationTableTestCase(unittest.TestCase):
    def testTable(self):
        t = pygrate.Table("employee", \
                [ pygrate.Number("id")
                , pygrate.String("name")
                ])

        self.assertEqual("employee",t.name())
        self.assertEqual(2,t.num_columns())

        i=0
        for c in t.columns():
            self.assertEqual(t.column(i).name(),c.name())
            i=i+1
