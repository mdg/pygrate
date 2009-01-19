import pygration


class PygrationDB:
    """A single step for a migration.
    """

    def __init__( self, db ):
        self._db

    def create_table( self, table_name, columns )
        self._db.create_table( table_name, columns )

    def hide_table( self, table_name )
        self._db.rename_table( table_name, "_hidden_"+ str(table_name) )

    def drop_table( self, table_name )
        self._db.drop_table( table_name, "_hidden_"+ str(table_name) )

    def add_column( self, table, column_obj )
        pass

    def hide_column( self, table_column_name )
        pass

    def drop_column( self, table_column_name )
        pass

    def execute_sql( self, sql ):
        self._db.execute_sql( sql )

    def execute_sql_file( self, sql_file ):
        self._db.execute_sql_file( sql_file )

