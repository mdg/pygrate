import pygrate
from pygrate import pygration
from pygrate.pygration import PygrationType
from pygrate.pygrator import Pygrator
import unittest


class TestPygration(pygrate.pygration.Pygration):
    def add( self ):
        pass


class PygrationTypeTestCase(unittest.TestCase):
    def test_pygration_not_subclass(self):
        p = pygrate.Pygration
        self.assertFalse( pygration.is_pygration_subclass(p) )

    def test_pygration_set_not_subclass(self):
        self.assertFalse( pygration.is_pygration_subclass( Pygrator ) )

    def test_pygration_subclass( self ):
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertTrue( pygration.is_pygration_subclass( tp ) )
        self.assertFalse( pygration.is_pygration_subclass( bp ) )
        self.assertFalse( pygration.is_pygration_subclass( dict ) )

