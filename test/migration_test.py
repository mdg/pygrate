import unittest
import os.path
from pygration.migration import VersionNumber, MigrationSet


class VersionComponentCompare(unittest.TestCase):
    """Test results for the component comparison function in Version."""
    def test_numeric_comparison(self):
        v = VersionNumber("v0")
        self.assertTrue( v._component_compare("1","2") < 0 )

    def test_numeric_comparison_double_digits(self):
        """Test that double digit numbers compare later than single digits."""
        v = VersionNumber("v0")
        self.assertTrue( v._component_compare("2","12") < 0 )


class VersionNumberTest(unittest.TestCase):
    """Tests for the pygration Version class."""

    def test_underscore_is_pygration(self):
        """Check that v0_0_0 is reported as a pygration version."""
        v = VersionNumber("v1_2_13")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "13")

    def test_dash_is_pygration(self):
        """Check that v0-0-0 is reported as a pygration version."""
        v = VersionNumber("v1-2-3")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "3")

    def test_dot_is_pygration(self):
        """Check that v0.0.0 is reported as a pygration version."""
        v = VersionNumber("v1.2.3")
        self.assertTrue( v.is_pygration() )
        self.assertEqual(v._component(0), "1")
        self.assertEqual(v._component(1), "2")
        self.assertEqual(v._component(2), "3")

    def test_asdf_is_not_pygration(self):
        """Assert that asdf is reported as not a pygration version."""
        v = VersionNumber("asdf")
        self.assertFalse( v.is_pygration() )

    def test_extended_version(self):
        """Test that a version with a sub-build number is compared later"""
        v1 = VersionNumber("v1")
        v2 = VersionNumber("v1-2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_numeric_compare(self):
        """Test that a numeric version is compared as a number."""
        v1 = VersionNumber("v1-2")
        v2 = VersionNumber("v1-12")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_underscore_comparison(self):
        v1 = VersionNumber("v0_1_2")
        v2 = VersionNumber("v0_2_2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_dash_comparison(self):
        v1 = VersionNumber("v0-1-2")
        v2 = VersionNumber("v0-2-2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_dot_comparison(self):
        v1 = VersionNumber("v0.1.2")
        v2 = VersionNumber("v0.2.2")
        self.assertTrue( cmp(v1, v2) < 0 )
        self.assertTrue( cmp(v2, v1) > 0 )

    def test_self_comparison(self):
        v = VersionNumber("v0.1.2")
        self.assertTrue( cmp(v, v) == 0 )

    def test_equality_comparison(self):
        vA = VersionNumber("v001")
        vB = VersionNumber("v001")
        self.assertTrue(vA == vB)


class MigrationSetTest(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        self._set = MigrationSet(test_dir)

    def test_find_versions(self):
        v001 = VersionNumber('v001')
        v002 = VersionNumber('v002')
        v07 = VersionNumber('v0-7')
        self.assertEqual([v07, v001, v002], self._set.find_migrations())

