import database
import pg_syntax
import pg


class PygresqlConnection(database.Connection):
    """An oracle database connection wrapper."""

    def __init__(self, opts):
        database.Connection.__init__(self, pg_syntax.PgSyntax())
        db = opts['database']
        user = opts['prospekz_dba']
        passwd = opts['passwd']
        self._conn = pg.connect(dbname=db, user=user, passwd=passwd)

    def close( self ):
        """Close this pygresql connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute_sql( self, sql ):
        self._last_sql = sql
        self._conn.query(sql)

