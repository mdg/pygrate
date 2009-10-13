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
        self.sql_command = list()

    def sql(self, cmd):
        self.command.append(cmd)
        self.sql_command.append(cmd)
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

    def simdrop(self, db):
        db.sql("create mock;")

    def rollback_simdrop(self, db):
        db.sql("drop mock;")

    def drop(self, db):
        db.sql("drop mock;")


class StepMigratorTest(unittest.TestCase):
    """Tests for the StepMigrator class"""
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

class StepMigratorPhaseCompleteTest(unittest.TestCase):
    def setUp(self):
        v = pygration.migration.VersionNumber("v1")
        self.state = pygration.db.PygrationState(str(v)
                , MockStep.step_id, MockStep.step_name)
        self.mig = StepMigrator(v, MockStep(), self.state)

    def test_phase_complete_new(self):
        self.assertFalse(self.mig.phase_complete('add'))
        self.assertFalse(self.mig.phase_complete('simdrop'))
        self.assertFalse(self.mig.phase_complete('drop'))

    def test_phase_complete_added(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        self.assertTrue(self.mig.phase_complete('add'))
        self.assertFalse(self.mig.phase_complete('simdrop'))
        self.assertFalse(self.mig.phase_complete('drop'))

    def test_phase_complete_simdropped(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        self.state.simdrop_state = pygration.migrator.STEP_PHASE_PASS
        self.assertTrue(self.mig.phase_complete('add'))
        self.assertTrue(self.mig.phase_complete('simdrop'))
        self.assertFalse(self.mig.phase_complete('drop'))

    def test_phase_complete_dropped(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        self.state.simdrop_state = pygration.migrator.STEP_PHASE_PASS
        self.state.drop_state = pygration.migrator.STEP_PHASE_PASS
        self.assertTrue(self.mig.phase_complete('add'))
        self.assertTrue(self.mig.phase_complete('simdrop'))
        self.assertTrue(self.mig.phase_complete('drop'))


class StepMigratorReadyToMigrateTest(unittest.TestCase):
    def setUp(self):
        v = pygration.migration.VersionNumber("v1")
        self.state = pygration.db.PygrationState(str(v)
                , MockStep.step_id, MockStep.step_name)
        self.mig = StepMigrator(v, MockStep(), self.state)

    def test_ready_to_migrate_new(self):
        print "mig = %s" % repr(self.mig)
        self.assertTrue(self.mig.ready_to_migrate('add'))
        self.assertFalse(self.mig.ready_to_migrate('simdrop'))
        self.assertFalse(self.mig.ready_to_migrate('drop'))

    def test_ready_to_migrate_added(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        print "mig = %s" % repr(self.mig)
        self.assertFalse(self.mig.ready_to_migrate('add'))
        self.assertTrue(self.mig.ready_to_migrate('simdrop'))
        self.assertFalse(self.mig.ready_to_migrate('drop'))

    def test_ready_to_migrate_simdropped(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        self.state.simdrop_state = pygration.migrator.STEP_PHASE_PASS
        print "mig = %s" % repr(self.mig)
        self.assertFalse(self.mig.ready_to_migrate('add'))
        self.assertFalse(self.mig.ready_to_migrate('simdrop'))
        self.assertTrue(self.mig.ready_to_migrate('drop'))

    def test_ready_to_migrate_dropped(self):
        self.state.add_state = pygration.migrator.STEP_PHASE_PASS
        self.state.simdrop_state = pygration.migrator.STEP_PHASE_PASS
        self.state.drop_state = pygration.migrator.STEP_PHASE_PASS
        print "mig = %s" % repr(self.mig)
        self.assertFalse(self.mig.ready_to_migrate('add'))
        self.assertFalse(self.mig.ready_to_migrate('simdrop'))
        self.assertFalse(self.mig.ready_to_migrate('drop'))


class StepMigratorCompleteThroughPhase(unittest.TestCase):
    def test_complete_through_phase(self):
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

        self.assertEqual(2, len(self._db.sql_command))
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
            self.assertEqual("Prerequisite phase for v0-7.EmployeeTable.drop" \
                    " is incomplete", str(x))
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

        self.assertEqual(6, len(self._db.sql_command))


class MigratorSingleStepTest(unittest.TestCase):
    def setUp(self):
        test1_dir = os.path.join(os.path.dirname(__file__), "test1")
        mset = pygration.migration.load(test1_dir)
        hist = History([])
        self.db = MockDB("pass")
        self.mig = Migrator(self.db, mset, hist)

    def test_migrate_single_step(self):
        "Test that an individual step can be run"
        self.mig.migrate('add', 'v0-7', 'EmployeeTable')

        self.assertEqual(1, len(self.db.sql_command))
        self.assertEqual("""
                CREATE TABLE employee2
                ( id number
                , txt_val varchar2(79)
                );
                """, self.db.sql_command[0])

    def test_migrate_single_out_of_order(self):
        "Test for failure when single migrations out of order"
        try:
            self.mig.migrate('add', 'v0-7', 'EmployeeValueIndex')
        except Exception, x:
            self.assertEqual(0, len(self.db.command))
            self.assertEqual("Prerequisite step 'v0-7.EmployeeTable' is not " \
                    "complete through 'add' phase", str(x))
        else:
            self.fail("Migrating steps out of order should have failed")

    def test_rollback_single_step(self):
        "Test that a single step can be rolled back"
        self.mig.migrate('add', 'v0-7')
        self.db.reset()
        self.mig.rollback('add', 'v0-7', 'EmployeeValueIndex')

        self.assertEqual(1, len(self.db.sql_command))
        self.assertEqual('DROP INDEX employee2idx;', self.db.sql_command[0])

    def test_rollback_single_out_of_order(self):
        "Test for failure when single rollback out of order"
        self.mig.migrate('add', 'v0-7')
        self.db.reset()
        try:
            self.mig.rollback('add', 'v0-7', 'EmployeeTable')
        except Exception, x:
            self.assertEqual(0, len(self.db.command))
            self.assertEqual("Subsequent step v0-7.EmployeeValueIndex must" \
                    " be rolled back before step v0-7.EmployeeTable", str(x))
        else:
            self.fail("Rollbacking steps out of order should have failed")


class MigratorSelectionTestCase(unittest.TestCase):
    def setUp(self):
        test1_dir = os.path.join(os.path.dirname(__file__), "test1")
        mset = pygration.migration.load(test1_dir)
        hist = History([])
        self._db = MockDB("pass")
        self._mig = Migrator(self._db, mset, hist)

    def test_migration_steps(self):
        steps = [s for s in self._mig._migration_steps('v001')]

        self.assertEqual(2, len(steps))
        self.assertEqual('v001', steps[0].version())
        self.assertEqual('SalaryTable', steps[0].step_name())
        self.assertEqual('v001', steps[1].version())
        self.assertEqual('EmployeeTable', steps[1].step_name())

    def test_single_migration_step(self):
        steps = [s for s in self._mig._migration_steps('v001', 'EmployeeTable')]

        self.assertEqual(1, len(steps))
        self.assertEqual('v001', steps[0].version())
        self.assertEqual('EmployeeTable', steps[0].step_name())

