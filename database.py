

class Database:
    """An actual database
    """

    def create_table_sql( self, table_name, columns ):
        pass

    def rename_table_sql( self, old_table_name, new_table_name ):
        pass

    def drop_table_sql( self, table_name ):
        pass

    def add_column_sql( self, table, column_obj ):
        pass

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass

    def execute_sql( self, sql ):
        pass

