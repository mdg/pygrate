import pygrate.pygrate
import unittest
import os.path
import sys


class PygrateTestCase(unittest.TestCase):
    def testListMigrations( self ):
        path, file = os.path.split( __file__ )
        p = pygrate.pygrate.Pygrator( path, 'r1' )
        m = p._list_migrations()

        self.assertEqual( [ 'employee' ], m )

    def testImportMigrations( self ):
        path, file = os.path.split( __file__ )
        p = pygrate.pygrate.Pygrator( path, 'r1' )
        p._import_migrations()
        print dir(p._modules)

