import database


class OracleDatabase(database.Database):
    """An oracle database
    """

    def __init__( self ):
        self._last_sql = ""

    def close( self ):
        pass

    def last_sql( self ):
        return self._last_sql

    def create_table_sql( self, table_name, columns ):
        sql = "CREATE TABLE %s" % ( table_name )
        column_prefix = '( '
        for c in columns:
            sql += "\n\t%s%s %s" % ( column_prefix, c.type(), c.name() )
            column_prefix = ', '
        sql += "\n\t);"
        return sql

    def rename_table_sql( self, old_table_name, new_table_name ):
        sql = "ALTER TABLE %s RENAME TO %s;" % \
                ( old_table_name, new_table_name )
        return sql

    def add_column_sql( self, table, column_obj ):
        pass

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass

    def execute_sql( self, sql ):
        self._last_sql = sql

