import pygrate.loader
import pygrate.pygration
import pygrate.oracle_syntax
import mock_database
import unittest
import os.path
import sys


class TestPygration(pygrate.pygration.Pygration):
    def add( self ):
        pass


class PygrateTestCase(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.dirname( __file__ )
        self._loader = pygrate.loader.PygrationLoader( test_dir, 'r1' )
        syntax = pygrate.oracle_syntax.OracleSyntax()

    def testListPygrationFiles( self ):
        files = self._loader._list_pygration_files()

        self.assertEqual( [ 'employee' ], files )

    def testImportModules( self ):
        self._loader._import_modules()
        print dir(self._loader._modules)

    def testLoad( self ):
        pass

    def testPygrationSubclass( self ):
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertEqual( True, self._loader._pygration_subclass( tp ) )
        self.assertEqual( False, self._loader._pygration_subclass( bp ) )
        self.assertEqual( False, self._loader._pygration_subclass( dict ) )

