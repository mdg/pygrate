import pygrate
from pygrate import pygration
from pygrate.pygration import PygrationType
from pygrate.pygration_set import PygrationSet
import unittest


class TestPygration(pygrate.pygration.Pygration):
    def add( self ):
        pass


class PygrationTypeTestCase(unittest.TestCase):
    def test_pygration_not_subclass(self):
        p = pygrate.Pygration
        self.assertFalse( pygration.is_pygration_subclass(p) )

    def test_pygration_set_not_subclass(self):
        self.assertFalse( pygration.is_pygration_subclass( PygrationSet ) )

    def test_pygration_subclass( self ):
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertTrue( pygration.is_pygration_subclass( tp ) )
        self.assertFalse( pygration.is_pygration_subclass( bp ) )
        self.assertFalse( pygration.is_pygration_subclass( dict ) )
                

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
