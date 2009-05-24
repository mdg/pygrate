import pygrate


class PygrationDB:
    """The user's interface to the DB from an implemented Pygration."""

    def __init__( self, db_conn ):
        self._db = db_conn
        self._syntax = db_conn.syntax()
        self._verbose = True

    def add(self, obj):
        """Add the object to the schema."""
        if isinstance(obj, pygrate.Table):
            table_name = obj.name()
            sql = self._syntax.create_table_sql(obj)
            self.execute_sql( sql )
        else:
            print "add unknown object %s" % repr(obj)

    def drop(self, obj):
        """Drop an object from the schema."""
        if isinstance(obj, pygrate.Table):
            table_name = obj.name()
            sql = self._syntax.drop_table_sql( "_hidden_"+ table_name )
            self.execute_sql( sql )
        else:
            print "drop unknown object %s" % repr(obj)

    def create_table( self, table_name, columns ):
        sql = self._syntax.create_table_sql( table_name, columns )
        self.execute_sql( sql )

    def drop_table( self, table_name ):
        """Hide a table before deleting it."""
        sql = self._syntax.rename_table_sql( table_name, "_hidden_"
                + str(table_name) )
        self.execute_sql( sql )

    def commit_drop_table( self, table_name ):
        """Drop a table that was previously hidden."""
        sql = self._syntax.drop_table_sql( "_hidden_"+ str(table_name) )
        self.execute_sql( sql )

    def table_exists(self, table_name):
        sql = self._syntax.table_exists_sql(table_name)
        self.execute_sql(sql)

    def add_column( self, table, column_obj ):
        """Add a column."""
        sql = self._syntax.add_column_sql( table, column_obj )
        self.execute_sql( sql )

    def hide_column( self, table_column_name ):
        table, column = self._split_table_column( table_column_name )
        sql = self._syntax.rename_column_sql( table, column, "_hidden"+ column )
        self.execute_sql( sql )

    def drop_column( self, table_column_name ):
        table, column = self._split_table_column( table_column_name )
        sql = self._syntax.drop_column_sql( table, "_hidden_"+ column )
        self.execute_sql( sql )

    def execute_sql( self, sql ):
        # write sql to the log
        if self._verbose:
            print "Run SQL:\n%s" % (sql)
        self._db.execute_sql( sql )

    def execute_sql_file( self, sql_file_name ):
        sql_file = open( sql_file_name )
        sql_file_string = sql_file.read()
        sql_file.close()
        self.execute_sql( sql_file_string )

    def _split_table_column( self, table_column_name ):
        """Split a table.column string into separate table & column strings
        """
        split_strings = table_column_name.split('.', 1)
        table = split_strings[0]
        column = split_strings[1]
        return table, column


class AddPygrationDB(PygrationDB):
    """PygrationDB for the add step."""

    def add(self, obj):
        """Add the object to the schema."""
        if isinstance(obj, pygrate.Table):
            sql = self._syntax.create_table_sql(obj)
            self.execute_sql(sql)
        else:
            print "add unknown object %s" % str(obj)

class DropPygrationDB(PygrationDB):
    """PygrationDB for the drop step."""

    def drop(self, obj):
        """Drop the object to the schema."""
        if isinstance(obj, pygrate.Table):
            sql = self._syntax.drop_table_sql(obj)
            self.execute_sql(sql)
        else:
            print "drop unknown object %s" % str(obj)

class CommitPygrationDB(PygrationDB):
    """PygrationDB to commit changes."""

    def drop(self, obj):
        """Commit a dropped object to the schema."""
        if isinstance(obj, pygrate.Table):
            sql = self._syntax.drop_table_sql(obj)
            self.execute_sql(sql)
        else:
            print "commit drop of unknown object %s" % str(obj)

class RollbackPygrationDB(PygrationDB):
    """PygrationDB to rollback changes."""

    def add(self, obj):
        """Rollback an added object."""
        if isinstance(obj, pygrate.Table):
            sql = self._syntax.drop_table_sql(obj)
            self.execute_sql(sql)
        else:
            print "rollback an unknown added object %s" % str(obj)

    def drop(self, obj):
        """Rollback a dropped object from the schema."""
        if isinstance(obj, pygrate.Table):
            sql = self._syntax.drop_table_sql(obj)
            self.execute_sql(sql)
        else:
            print "rollback an unknown dropped object %s" % str(obj)

