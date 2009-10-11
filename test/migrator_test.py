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
        self._action = action
        self.reset()

    def reset(self):
        self.command = list()

    def sql(self, cmd):
        self.command.append(cmd)
        if self._action == "pass":
            pass

    def commit(self, state):
        self.command.append("commit()")

@pygration.step_class
class MockStep(object):
    def add(self, db):
        db.sql("create mock;")

    def rollback_add(self, db):
        db.sql("drop mock;")


class StepMigratorTest(unittest.TestCase):
    def test_normal_add_pass(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id, MockStep.step_name)
        mig = StepMigrator(v, MockStep(), state)
        db = MockDB("pass")
        result = mig.migrate(db, "add")

        self.assertEqual("P", result.add_state)

    def test_normal_rollback_add(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id, MockStep.step_name)
        mig = StepMigrator(v, MockStep(), state)
        db = MockDB("pass")
        result = mig.rollback(db, "add")

        self.assertEqual("RB", mig._state.add_state)
        self.assertEqual(2, len(db.command))
        self.assertEqual("drop mock;", db.command[0])
        self.assertEqual("commit()", db.command[1])

    def test_phase_complete(self):
        v = pygration.migration.VersionNumber("v1-5")
        state = pygration.db.PygrationState(str(v)
                , MockStep.step_id, MockStep.step_name)
        mig = StepMigrator(v, MockStep(), state)

        self.assertFalse(mig.phase_complete('add'))
        self.assertFalse(mig.phase_complete('simdrop'))
        self.assertFalse(mig.phase_complete('drop'))


class MigratorTest(unittest.TestCase):
    def setUp(self):
        test1_dir = os.path.join(os.path.dirname(__file__), "test1")
        mset = pygration.migration.load(test1_dir)
        hist = History([])
        self._db = MockDB("pass")
        self._test1_migrator = Migrator(self._db, mset, hist)

    def test_migrate_add(self):
        mig = self._test1_migrator
        mig.migrate('add', 'v0-7')

        self.assertEqual(2, len(self._db.command))
        self.assertEqual("""
                CREATE TABLE employee2
                ( id number
                , txt_val varchar2(79)
                );
                """, self._db.command[0])
        self.assertEqual('commit()', self._db.command[1])

    def test_migrate_phase_out_of_order(self):
        """Test if the drop phase is run before the add phase"""
        mig = self._test1_migrator
        try:
            mig.migrate('drop', 'v0-7')
        except Exception, x:
            self.assertEqual("Prerequisite step is incomplete: " \
                    "'v0-7.EmployeeTable'", str(x))
            self.assertEqual(0, len(self._db.command))
        else:
            self.fail("Dropping before adding should have failed.""")

    def test_migrations_out_of_order(self):
        """Test for error when migrating out of order

        Migrations should not be complete if running out of order."""
        mig = self._test1_migrator

        try:
            mig.migrate('add', 'v001')
        except Exception, x:
            # expected, this is good
            self.assertEqual(0, len(self._db.command))
            self.assertEqual("Prerequisite migration is incomplete: 'v0-7'"
                    , str(x))
        else:
            self.fail("migration out of order should have thrown an error")

    def test_rollback_after_drop(self):
        """Test for error when rolling back simdrop after drop"""
        mig = self._test1_migrator

        mig.migrate('add', 'v0-7')
        mig.migrate('simdrop', 'v0-7')
        mig.migrate('drop', 'v0-7')
        self._db.reset()
        try:
            mig.rollback('simdrop', 'v0-7')
        except Exception, x:
            # expected, this is good
            self.assertEqual("Cannot rollback past dropped steps", str(x))
            self.assertEqual(0, len(self._db.command))
        else:
            self.fail("migration out of order should have thrown an error")

    def test_rollback_drop_fails(self):
        """Test for error when trying to rollback drop"""
        mig = self._test1_migrator

        mig.migrate('add', 'v0-7')
        mig.migrate('simdrop', 'v0-7')
        mig.migrate('drop', 'v0-7')
        self._db.reset()
        try:
            mig.rollback('drop', 'v0-7')
        except Exception, x:
            # expected, this is good
            self.assertEqual("Drop phase cannot be rolled back", str(x))
            self.assertEqual(0, len(self._db.command))
        else:
            self.fail("migration out of order should have thrown an error")

    def test_add_without_prior_drop(self):
        """Test what happens if MigB.add is called before MigA.drop"""
        mig = self._test1_migrator

        mig.migrate('add', 'v0-7')
        self._db.reset()
        try:
            mig.migrate('add', 'v001')
        except Exception, x:
            self.assertEqual(0, len(self._db.command))
            self.assertEqual("Prerequisite migration is incomplete: 'v0-7'"
                    , str(x))
        else:
            self.fail("adding without drop of previous migration " \
                    "should have failed")

    def test_migrate_nonexistent_version(self):
        """Test that migrator handles invalid version number"""
        mig = self._test1_migrator

        try:
            mig.migrate('drop', 'v0-8')
        except Exception, x:
            # expected, this is good
            self.assertEqual(0, len(self._db.command))
            self.assertEqual("Invalid migration version: 'v0-8'", str(x))
        else:
            self.fail("invalid version should have thrown an error")

    def test_fastforward(self):
        """Test fast-forward feature"""
        self._test1_migrator.fastforward()

        noncommits = [c for c in self._db.command if c != "commit()"]
        self.assertEqual(5, len(noncommits))

