import database


class MockDatabase(database.Database):
    """An actual database
    """

    def __init__( self ):
        self._last_sql = ""

    def last_sql( self ):
        return self._last_sql

    def create_table_sql( self, table_name, columns ):
        sql = "create table "+ table_name +" ("
        for c in columns:
            sql += c.type() +" "+ c.name() +", "
        sql += ")"
        return sql

    def rename_table( self, old_table_name, new_table_name ):
        pass

    def drop_table( self, table_name ):
        pass

    def add_column( self, table, column_obj ):
        pass

    def rename_column( self, table, old_name, new_name ):
        pass

    def drop_column( self, table, column_name ):
        pass

    def execute_sql( self, sql ):
        self._last_sql = sql

