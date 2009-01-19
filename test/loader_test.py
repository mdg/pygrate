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
        path, file = os.path.split( __file__ )
        p = pygrate.loader.PygrationLoader( path, 'r1' )
        m = p._list_pygration_files()

        self.assertEqual( [ 'employee' ], m )

    def testImportModules( self ):
        path, file = os.path.split( __file__ )
        p = pygrate.loader.PygrationLoader( path, 'r1' )
        p._import_modules()
        print dir(p._modules)

    def testPygrationSubclass( self ):
        p = pygrate.loader.PygrationLoader( self._test_dir, 'r1' )
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertEqual( True, p._pygration_subclass( tp ) )
        self.assertEqual( False, p._pygration_subclass( bp ) )
        self.assertEqual( False, p._pygration_subclass( dict ) )

