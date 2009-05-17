import database


class PgSyntax(database.Syntax):
    """PostgreSQL syntax formatter"""

    def create_table_sql( self, table ):
        """Format a postgres create table command."""

        sql = "CREATE TABLE %s" % ( table.name() )
        column_prefix = '( '
        for c in table.columns():
            sql += "\n\t%s%s %s" % ( column_prefix, c.name()
                    , c.postgres_type() )
            column_prefix = ', '
        sql += "\n\t);"
        return sql

    def rename_table_sql( self, old_table_name, new_table_name ):
        """Format a postgres statement to rename a table."""

        sql = "ALTER TABLE %s RENAME TO %s;" % \
                ( old_table_name, new_table_name )
        return sql

    def add_column_sql( self, table, column_obj ):
        """Format a postgres statement to add a column to a table."""
        print "PgSyntax.add_column_sql"

        sql = "ALTER TABLE %s ADD %s %s;" % ( table, column_obj.postgres_type()
                , column_obj.name() )
        return sql

    def rename_column_sql( self, table, old_name, new_name ):
        pass

    def drop_column_sql( self, table, column_name ):
        pass

