import pygrate.loader
import pygrate.pygration
from pygrate.pygration import PygrationType
from pygrate.loader import Version
import unittest
import os.path
import types


class VersionFinderTestCase(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        self._finder = pygrate.loader.VersionFinder( test_dir )

    def test_find_versions(self):
        v001 = Version('v001')
        v002 = Version('v002')
        v07 = Version('v0-7')
        self.assertEqual([v07, v001, v002], self._finder.find_versions())


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


class VersionComponentCompare(unittest.TestCase):
    """Test results for the component comparison function in Version."""
    def test_numeric_comparison(self):
        v = pygrate.loader.Version("v0")
        self.assertTrue( v._component_compare("1","2") < 0 )

    def test_numeric_comparison_double_digits(self):
        """Test that double digit numbers compare later than single digits."""
        v = pygrate.loader.Version("v0")
        self.assertTrue( v._component_compare("2","12") < 0 )

class VersionTestCase(unittest.TestCase):
    """Tests for the pygration Version class."""

    def test_underscore_is_pygration(self):
        """Check that v0_0_0 is reported as a pygration version."""
        v = pygrate.loader.Version("v1_2_13")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "13")

    def test_dash_is_pygration(self):
        """Check that v0-0-0 is reported as a pygration version."""
        v = pygrate.loader.Version("v1-2-3")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "3")

    def test_dot_is_pygration(self):
        """Check that v0.0.0 is reported as a pygration version."""
        v = pygrate.loader.Version("v1.2.3")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "3")

    def test_asdf_is_not_pygration(self):
        """Assert that asdf is reported as not a pygration version."""
        v = pygrate.loader.Version("asdf")
        self.assertFalse( v.is_pygration() )

    def test_extended_version(self):
        """Test that a version with a sub-build number is compared later"""
        v1 = pygrate.loader.Version("v1")
        v2 = pygrate.loader.Version("v1-2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_numeric_compare(self):
        """Test that a numeric version is compared as a number."""
        v1 = pygrate.loader.Version("v1-2")
        v2 = pygrate.loader.Version("v1-12")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_underscore_comparison(self):
        v1 = pygrate.loader.Version("v0_1_2")
        v2 = pygrate.loader.Version("v0_2_2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_dash_comparison(self):
        v1 = pygrate.loader.Version("v0-1-2")
        v2 = pygrate.loader.Version("v0-2-2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_dot_comparison(self):
        v1 = pygrate.loader.Version("v0.1.2")
        v2 = pygrate.loader.Version("v0.2.2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_self_comparison(self):
        v = pygrate.loader.Version("v0.1.2")
        self.assertTrue( cmp(v, v) == 0 )

    def test_equality_comparison(self):
        vA = Version("v001")
        vB = Version("v001")
        self.assertTrue(vA == vB)

