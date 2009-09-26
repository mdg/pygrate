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
        self.command.append("commit()")

class MockStep(pygration.Step):
    def add(self, db):
        db.sql("create mock;")

    def rollback_add(self, db):
        db.sql("drop mock;")


class StepMigratorTest(unittest.TestCase):
    def test_normal_add_pass(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id(), MockStep.step_name())
        mig = StepMigrator(v, MockStep, state)
        db = MockDB("pass")
        result = mig.migrate(db, "add")

        self.assertEqual("P", result.add_state)

    def test_normal_rollback_add(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id(), MockStep.step_name())
        mig = StepMigrator(v, MockStep, state)
        db = MockDB("pass")
        result = mig.rollback(db, "add")

        self.assertEqual("RB", mig._state.add_state)
        self.assertEqual(2, len(db.command))
        self.assertEqual("drop mock;", db.command[0])
        self.assertEqual("commit()", db.command[1])


class MigratorTest(unittest.TestCase):
    def setUp(self):
        test1_dir = os.path.join(os.path.dirname(__file__), "test1")
        mset = pygration.migration.load(test1_dir)
        hist = History([])
        self._db = MockDB("pass")
        self._test1_migrator = Migrator(self._db, mset, hist)

    def test_migrate_drop(self):
        mig = self._test1_migrator
        mig.migrate('drop', 'v0-7')

        self.assertEqual(2, len(self._db.command))
        self.assertEqual('DROP TABLE old_employee', self._db.command[0])
        self.assertEqual('commit()', self._db.command[1])

    def test_migrate_nonexistent_version(self):
        """Test that migrator handles invalid version number"""
        mig = self._test1_migrator

        try:
            mig.migrate('drop', 'v0-8')
        except:
            # expected, this is good
            self.assertEqual(0, len(self._db.command))
        else:
            self.fail("invalid version should have thrown an error")


