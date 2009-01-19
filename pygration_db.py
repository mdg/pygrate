import pygration


class PygrationDB:
    """A single step for a migration.
    """

    def __init__( self, db ):
        self._db

    def create_table( self, table_name, columns )
        self._db.create_table( table_name, columns )

    def hide_table( self, table_name )
        """Hide a table before deleting it."""
        self._db.rename_table( table_name, "_hidden_"+ str(table_name) )

    def drop_table( self, table_name )
        """Drop a hidden table."""
        self._db.drop_table( "_hidden_"+ str(table_name) )

    def add_column( self, table, column_obj )
        self._db.add_column( table, column_obj )

    def hide_column( self, table_column_name )
        table, column = self.split_table_column( table_column_name )
        self._db.rename_column( table, column, "_hidden"+ column )

    def drop_column( self, table_column_name )
        table, column = self.split_table_column( table_column_name )
        self._db.drop_column( table, "_hidden_"+ column )

    def execute_sql( self, sql ):
        self._db.execute_sql( sql )

    def execute_sql_file( self, sql_file ):
        self._db.execute_sql_file( sql_file )

    def _split_table_column( self, table_column_name ):
        """Split a table.column string into separate table & column strings
        """
        split_strings = table_column_name.split('.', 1)
        table = split_strings[0]
        column = split_strings[1]
        return table, column

