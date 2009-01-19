import pygrate.loader
import pygrate.pygration
import unittest
import os.path
import types


class TestPygration(pygrate.pygration.Pygration):
    def add( self ):
        pass


class PygrateTestCase(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.dirname( __file__ )
        self._loader = pygrate.loader.PygrationLoader( test_dir, 'r1' )
        syntax = pygrate.oracle_syntax.OracleSyntax()

    def testListModules( self ):
        modules = self._loader._list_modules()

        self.assertEqual( [ 'employee' ], modules )

    def testImportModules( self ):
        self._loader._import_modules()
        m = self._loader._modules
        self.assertEqual( 1, len(m) )
        self.assertEqual( types.ModuleType, type(m[0]) )

    def testLoad( self ):
        self._loader.load()
        p = self._loader.pygrations()

        self.assertEqual( 1, len(p) )
        self.assertTrue( isinstance( p[0], pygrate.pygration.Pygration ) )

    def testPygrationSubclass( self ):
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertTrue( self._loader._pygration_subclass( tp ) )
        self.assertFalse( self._loader._pygration_subclass( bp ) )
        self.assertFalse( self._loader._pygration_subclass( dict ) )

