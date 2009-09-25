import unittest
import os.path
import pygration
from pygration.migrator import StepMigrator, Migrator
from pygration.history import History
import pygration.migration
import pygration.db


class MockDB(object):
    """Mock for the pygration DB objects."""
    def __init__(self, action):
        self.command = []
        self._action = action

    def sql(self, cmd):
        self.command.append(cmd)
        if self._action == "pass":
            pass

    def commit(self, state):
        pass

class MockStep(pygration.Step):
    def add(self, db):
        db.sql("create mock;")


class StepMigratorTest(unittest.TestCase):
    def test_normal_add_pass(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id(), MockStep.step_name())
        mig = StepMigrator(v, MockStep, state)
        db = MockDB("pass")
        result = mig.migrate(db, "add")

        self.assertEqual("P", result.add_state)


class MigratorTest(unittest.TestCase):
    def setUp(self):
        self._test1_dir = os.path.join(os.path.dirname(__file__), "test1")

    def test_migrate_add(self):
        db = MockDB("pass")
        mset = pygration.migration.load(self._test1_dir)
        hist = History([])
        mig = Migrator(db, mset, hist)

        mig.migrate('drop', 'v0-7')

        self.assertEqual(1, len(db.command))
        self.assertEqual('DROP TABLE old_employee', db.command[0])

