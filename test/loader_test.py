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
        self._test_dir = os.path.dirname( __file__ )
        syntax = pygrate.oracle_syntax.OracleSyntax()

    def testListPygrationFiles( self ):
        l = pygrate.loader.PygrationLoader( self._test_dir, 'r1' )
        m = l._list_pygration_files()

        self.assertEqual( [ 'employee' ], m )

    def testImportModules( self ):
        l = pygrate.loader.PygrationLoader( self._test_dir, 'r1' )
        l._import_modules()
        print dir(l._modules)

    def testLoad( self ):
        pass

    def testPygrationSubclass( self ):
        l = pygrate.loader.PygrationLoader( self._test_dir, 'r1' )
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertEqual( True, l._pygration_subclass( tp ) )
        self.assertEqual( False, l._pygration_subclass( bp ) )
        self.assertEqual( False, l._pygration_subclass( dict ) )

