import unittest
import os.path
from pygration.migrator import StepMigrator, Migrator
from pygration.history import History
import pygration.migration


class MockDB(object):
    """Mock for the pygration DB objects."""
    def __init__(self):
        self.command = []

    def sql(self, cmd):
        self.command.append(cmd)

    def commit(self, state):
        pass


class StepMigratorTest(unittest.TestCase):
    pass


class MigratorTest(unittest.TestCase):
    def setUp(self):
        self._test1_dir = os.path.join(os.path.dirname(__file__), "test1")

    def test_migrate_add(self):
        db = MockDB()
        mset = pygration.migration.load(self._test1_dir)
        hist = History([])
        mig = Migrator(db, mset, hist)

        mig.migrate('drop', 'v0-7')

        self.assertEqual(1, len(db.command))
        self.assertEqual('DROP TABLE old_employee', db.command[0])

