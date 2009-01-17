
import pygration


class PygrationStep:
    """A single step for a migration.
    """

    def execute_sql( self, sql ):
        self._sql = sql

    def execute_sql_file( self, sql_file ):
        self._sql_file = sql_file


class Pygrator:
    """The operator for running a set of pygrations.
    """

    def __init__( self ):
        pass

