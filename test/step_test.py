import pygration
from pygration.step import pygration_step_subclass
import unittest


class TestStep(pygration.Step):
    ID = "5"

    def add( self ):
        pass

class TestStep3(pygration.Step):
    def add( self ):
        pass


class StepTypeTestCase(unittest.TestCase):
    def test_step_not_subclass(self):
        p = pygration.Step
        self.assertFalse(pygration_step_subclass(p))

    def test_child_step_subclass( self ):
        child = TestStep
        base = pygration.Step
        dict = {}

        self.assertTrue( pygration_step_subclass( child ) )
        self.assertFalse( pygration_step_subclass( base ) )
        self.assertFalse( pygration_step_subclass( dict ) )


class StepTestCase(unittest.TestCase):
    def test_step_name(self):
        """Test that the step name is reported properly."""
        t = TestStep()

        self.assertEqual("TestStep", t.step_name())

    def test_explicit_step_id(self):
        """Test that the step ID is reported properly when set explicitly."""
        t = TestStep()
        self.assertEqual("5", t.step_id())

    def test_explicit_class_step_id(self):
        """Test that the step ID is reported properly by the class
        when set explicitly."""
        s = TestStep
        self.assertEqual("5", s.step_id())

    def test_implicit_step_id_for_instance(self):
        s = TestStep3()
        self.assertEqual("TestStep3", s.step_id())

