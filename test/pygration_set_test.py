from pygrate.pygration_set import PygrationSet
from pygrate.pygration import Pygration
from pygrate.pygrator import Pygrator
from pygrate import database
import mock_pygrations
import unittest


class PygrationTracker(Pygration):
    def __init__(self):
        self._sequence = []

    def add(self,db):
        self._sequence.append('add')

    def hide(self,db):
        self._sequence.append('hide')

    def drop(self,db):
        self._sequence.append('drop')

    def rollback_add(self,db):
        self._sequence.append('rollback_add')

    def rollback_hide(self,db):
        self._sequence.append('rollback_hide')


class PygrationSetTestCase(unittest.TestCase):
    def setUp(self):
        self._pygration = [PygrationTracker()]
        self._set = PygrationSet(self._pygration)
        conn = database.Connection( database.Syntax() )
        self._pygrator = Pygrator( conn )

    def testAdd(self):
        self._set.migrate(self._pygrator,"add")

        self.assertTrue("add",self._pygration[0]._sequence)

