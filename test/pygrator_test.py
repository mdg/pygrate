from pygrate.pygrator import Pygrator
from pygrate.pygration import Pygration
from pygrate.pygration_db import PygrationDB
from pygrate import database
import mock_pygrations
import unittest


class PygrationTracker(object):
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


class PygratorTestCase(unittest.TestCase):
    def setUp(self):
        self._pygration = [PygrationTracker()]
        self._pygrator = Pygrator(self._pygration)
        conn = database.Connection( database.Syntax() )
        self._db = PygrationDB( conn )

    def testAdd(self):
        self._pygrator.migrate(self._db,"add")

        self.assertTrue("add",self._pygration[0]._operation)

    def testDrop(self):
        self._pygrator.migrate(self._db,"drop")

        self.assertTrue("drop",self._pygration[0]._operation)

    def testCommitDrop(self):
        self._pygrator.migrate(self._db,"commit_drop")

        self.assertTrue("commit_drop",self._pygration[0]._operation)

    def testRollbackAdd(self):
        self._pygrator.migrate(self._db,"rollback_add")

        self.assertTrue("rollback_add",self._pygration[0]._operation)

    def testRollbackDrop(self):
        self._pygrator.migrate(self._db,"rollback_drop")

        self.assertTrue("rollback_drop",self._pygration[0]._operation)

