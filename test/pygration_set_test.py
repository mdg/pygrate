from pygrate.pygration_set import PygrationSet
from pygrate.pygration import Pygration
from pygrate.pygrator import Pygrator
from pygrate import database
import mock_pygrations
import unittest


class PygrationTracker(Pygration):
    def __init__(self):
        self._operation = ''

    def add(self,db):
        self._operation = 'add'

    def hide(self,db):
        self._operation = 'drop'

    def drop(self,db):
        self._operation = 'commit_drop'

    def rollback_add(self,db):
        self._operation = 'rollback_add'

    def rollback_hide(self,db):
        self._operation = 'rollback_drop'


class PygrationSetTestCase(unittest.TestCase):
    def setUp(self):
        self._pygration = [PygrationTracker()]
        self._set = PygrationSet(self._pygration)
        conn = database.Connection( database.Syntax() )
        self._pygrator = Pygrator( conn )

    def testAdd(self):
        self._set.migrate(self._pygrator,"add")

        self.assertTrue("add",self._pygration[0]._operation)

    def testDrop(self):
        self._set.migrate(self._pygrator,"drop")

        self.assertTrue("drop",self._pygration[0]._operation)

    def testCommitDrop(self):
        self._set.migrate(self._pygrator,"commit_drop")

        self.assertTrue("commit_drop",self._pygration[0]._operation)

    def testRollbackAdd(self):
        self._set.migrate(self._pygrator,"rollback_add")

        self.assertTrue("rollback_add",self._pygration[0]._operation)

    def testRollbackDrop(self):
        self._set.migrate(self._pygrator,"rollback_drop")

        self.assertTrue("rollback_drop",self._pygration[0]._operation)

