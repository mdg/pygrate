
class Pygrator:
    """The user's interface to the DB from an implemented Pygration."""


    def __init__( self, db_conn ):
        self._db = db_conn
        self._syntax = db_conn.syntax()
        self._verbose = True

    def create( self, obj ):
        pass

    def create_table( self, table_name, columns ):
        sql = self._syntax.create_table_sql( table_name, columns )
        self.execute_sql( sql )

    def hide_table( self, table_name ):
        """Hide a table before deleting it."""
        sql = self._syntax.rename_table_sql( table_name, "_hidden_"
                + str(table_name) )
        self.execute_sql( sql )

    def drop_table( self, table_name ):
        """Drop a table that was previously hidden."""
        sql = self._syntax.drop_table_sql( "_hidden_"+ str(table_name) )
        self.execute_sql( sql )

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
        self._db.execute_sql_file( sql_file_string )
        sql_file.close()

    def _split_table_column( self, table_column_name ):
        """Split a table.column string into separate table & column strings
        """
        split_strings = table_column_name.split('.', 1)
        table = split_strings[0]
        column = split_strings[1]
        return table, column

