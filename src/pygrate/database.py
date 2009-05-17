

class Syntax:
    """Base class for formatting a DB command into actual SQL"""

    # Table commands
    def create_table_sql( self, table_name, columns ):
        pass

    def rename_table_sql( self, old_table_name, new_table_name ):
        pass

    def drop_table_sql( self, table_name ):
        """Generic syntax to drop a table."""
        sql = "DROP TABLE %s;" % ( table_name )
        return sql

    # Column commands
    def add_column_sql( self, table, column_obj ):
        pass

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass


class Connection:
    """Base class for a connected DB."""
    def __init__( self, syntax ):
        self._syntax = syntax
        self._last_sql = ''

    def close( self ):
        pass

    def syntax( self ):
        return self._syntax

    def execute_sql( self, sql ):
        """Execute SQL should be overridden by child classes."""
        pass

    def last_sql(self):
        return self._last_sql


def open( path ):
    """Open a database connection as configured at the given path."""
    return Connection( Syntax() )

