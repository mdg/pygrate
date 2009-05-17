import database
import pg_syntax


class PygresqlConnection(database.Connection):
    """An oracle database connection wrapper."""

    def __init__( self ):
        import pg
        database.Connection.__init__(self, pg_syntax.PgSyntax())
        self._conn = pg.connect(dbname='prospekz', user='prospekz_dba'
                , passwd='dba123')

    def close( self ):
        """Close this pygresql connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute_sql( self, sql ):
        self._last_sql = sql
        self._conn.query(sql)

