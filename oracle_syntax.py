import database


class OracleSyntax(database.Syntax):
    """Oracle syntax formatter"""

    def create_table_sql( self, table_name, columns ):
        sql = "CREATE TABLE %s" % ( table_name )
        column_prefix = '( '
        for c in columns:
            sql += "\n\t%s%s %s" % ( column_prefix, c.oracle_type(), c.name() )
            column_prefix = ', '
        sql += "\n\t);"
        return sql

    def rename_table_sql( self, old_table_name, new_table_name ):
        sql = "ALTER TABLE %s RENAME TO %s;" % \
                ( old_table_name, new_table_name )
        return sql

    def add_column_sql( self, table, column_obj ):
        sql = "ALTER TABLE %s ADD %s %s;" % ( table, column_obj.oracle_type()
                , column_obj.name() )
        return sql

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass

