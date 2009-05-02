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
        self._loader = pygrate.loader.PygrationLoader( test_dir, 'v1' )
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

    def testFindNewestVersion(self):
        newest = self._loader._find_newest_version()
        self.assertEqual( "v1", newest._string )

    def testPygrationSubclass( self ):
        tp = TestPygration
        bp = pygrate.pygration.Pygration
        dict = {}

        self.assertTrue( self._loader._pygration_subclass( tp ) )
        self.assertFalse( self._loader._pygration_subclass( bp ) )
        self.assertFalse( self._loader._pygration_subclass( dict ) )


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
        self.assertTrue( v1.compare(v2) < 0 )
        self.assertTrue( v2.compare(v1) > 0 )

    def test_numeric_compare(self):
        """Test that a numeric version is compared as a number."""
        v1 = pygrate.loader.Version("v1-2")
        v2 = pygrate.loader.Version("v1-12")
        self.assertTrue( v1.compare(v2) < 0 )
        self.assertTrue( v2.compare(v1) > 0 )

    def test_underscore_comparison(self):
        v1 = pygrate.loader.Version("v0_1_2")
        v2 = pygrate.loader.Version("v0_2_2")
        self.assertTrue( v1.compare(v2) < 0 )
        self.assertTrue( v2.compare(v1) > 0 )

    def test_dash_comparison(self):
        v1 = pygrate.loader.Version("v0-1-2")
        v2 = pygrate.loader.Version("v0-2-2")
        self.assertTrue( v1.compare(v2) < 0 )
        self.assertTrue( v2.compare(v1) > 0 )

    def test_dot_comparison(self):
        v1 = pygrate.loader.Version("v0.1.2")
        v2 = pygrate.loader.Version("v0.2.2")
        self.assertTrue( v1.compare(v2) < 0 )
        self.assertTrue( v2.compare(v1) > 0 )

    def test_self_comparison(self):
        v = pygrate.loader.Version("v0.1.2")
        self.assertTrue( v.compare(v) == 0 )

