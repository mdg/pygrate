
import pygration


class PygrationDB:
    """A single step for a migration.
    """

    def execute_sql( self, sql ):
        self._sql = sql

    def execute_sql_file( self, sql_file ):
        self._sql_file = sql_file

class AddPygrationDB(PygrationDB):
    """An operator class for adding elements to the DB.
    """

    def add_column( self, table, column ):
        pass

class HidePygrationDB(PygrationDB):
    """An operator class for hiding elements in the DB.
    """

    def hide_column( self, table_column ):
        pass

class DropPygrationDB(PygrationDB):
    """An operator class for dropping elements from the DB.
    """

    def drop_column( self, table_column ):
        pass


class Pygrator:
    """The operator for running a set of pygrations.
    """

    def __init__( self ):
        pass
