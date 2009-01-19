

class Syntax:
    """Base class for formatting a DB command into actual SQL"""

    def create_table_sql( self, table_name, columns ):
        pass

    def rename_table_sql( self, old_table_name, new_table_name ):
        pass

    def drop_table_sql( self, table_name ):
        """Generic syntax to drop a table."""
        sql = "DROP TABLE %s;" % ( table_name )
        return sql

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

    def close( self ):
        pass

    def syntax( self ):
        return self._syntax

    def execute_sql( self, sql ):
        pass


def open( path ):
    return Connection( Syntax() )

