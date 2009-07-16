import pygration
from pygration.step import pygration_step_subclass
import unittest


class TestStep(pygration.Step):
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

