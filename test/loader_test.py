import pygrate.loader
import pygrate.pygration
from pygrate.pygration import PygrationType
from pygrate.loader import Version
import unittest
import os.path
import types


class LoaderTestCase(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        self._loader = pygrate.loader.PygrationLoader( test_dir, 'v001' )

    def testImportModule(self):
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        l = pygrate.loader.PygrationLoader(test_dir, 'v001')
        l._import_module()

        m = l._modules
        self.assertEqual( 1, len(m) )
        self.assertEqual( types.ModuleType, type(m[0]) )

    def testLoad(self):
        initial_len = len(PygrationType.pygrations)
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        l = pygrate.loader.PygrationLoader(test_dir, 'v001')
        p = l.load()

        self.assertEqual( 2, len(p) )
        self.assertEqual(2, len(PygrationType.pygrations)-initial_len)
        self.assertEqual("SalaryTable", \
                PygrationType.pygrations[initial_len].__name__)
        self.assertEqual("EmployeeTable", \
                PygrationType.pygrations[initial_len+1].__name__)
        self.assertEqual("SalaryTable", p[0].__class__.__name__)
        self.assertEqual("EmployeeTable", p[1].__class__.__name__)
        # self.assertEqual([], PygrationType.pygrations)


class PygrationLoadErrorsTest(unittest.TestCase):
    """Test pygration loads with errors to verify error behavior."""
 
    """Test with a bad type to make sure the errors are nice."""
    def test_bad_type(self):
        test_dir = os.path.dirname( __file__ )
        loader = pygrate.loader.PygrationLoader( test_dir, 'v0-7' )
        loader.load()
        loader.pygrations()

    """Verify correct behavior when a given module doesn't exist."""
    def test_no_module(self):
        test_dir = os.path.dirname( __file__ )
        loader = pygrate.loader.PygrationLoader( test_dir, 'vasdf' )
        try:
            loader.load()
        except:
            # this should assert an exception was thrown somehow
            pass
        else:
            failure( "no exception" )
        loader.pygrations()

