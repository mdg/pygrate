import unittest
import os.path
import types
from pygration.migration import VersionNumber, Loader
import pygration


@pygration.step_class
class TestStep(object):
    ADD_FILE = 'add.sql'


class StepTest(unittest.TestCase):
    def test_class_decorator(self):
        self.assertEqual("test.migration_test", TestStep.version)
        self.assertEqual("TestStep", TestStep.step_name)
        self.assertEqual("TestStep", TestStep.step_id)


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
    pass


class LoaderTest(unittest.TestCase):
    def setUp( self ):
        test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )
        self._loader = Loader(test_dir)

    def test_find_versions(self):
        v001 = VersionNumber('v001')
        v002 = VersionNumber('v002')
        v07 = VersionNumber('v0-7')
        self._loader._find_files()
        self.assertEqual([v07, v001, v002], self._loader._find_versions())

    def test_load_migration_module(self):
        self._loader._load_migration_module('v001')

        m = self._loader._modules
        self.assertEqual( 1, len(m) )
        self.assertEqual( types.ModuleType, type(m[0]) )


class MigrationLoadTest(unittest.TestCase):
    def setUp( self ):
        self._test_dir = os.path.join( os.path.dirname( __file__ ), "test1" )

    def test_load(self):
        """Test that the migration loader loads correctly."""
        migset = pygration.migration.load(self._test_dir)
        migs = migset.migrations()

        self.assertEqual(3, len(migs))
        self.assertEqual("v0-7", migs[0].version())
        self.assertEqual("v001", migs[1].version())
        self.assertEqual("v002", migs[2].version())

        v07 = migs[0]
        self.assertEqual(2, len(v07.steps()))
        self.assertEqual("EmployeeTable", v07.step(0).step_name)

        v001 = migs[1]
        self.assertEqual(2, len(v001.steps()))
        self.assertEqual("SalaryTable", v001.step(0).step_name)
        self.assertEqual("EmployeeTable", v001.step(1).step_name)

        v002 = migs[2]
        self.assertEqual(1, len(v002.steps()))
        self.assertEqual("AccountTable", v002.step(0).step_name)

