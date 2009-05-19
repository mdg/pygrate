import database
import pg_syntax
import pg


class PygresqlConnection(database.Connection):
    """An oracle database connection wrapper."""

    def __init__(self, opts):
        database.Connection.__init__(self, pg_syntax.PgSyntax())
        # these values come from the given database.d config file
        db = host = user = password = None
        if 'database' in opts:
            db = opts['database']
        if 'host' in opts:
            host = opts['host']
        if 'user' in opts:
            user = opts['user']
        if 'password' in opts:
            password = opts['password']

        if True or 'verbose' in opts:
            print "pg.connect(dbname=%s, host=%s, user=%s, passwd=%s)" \
                    % (db, host, user, password)
        self._conn = pg.connect(dbname=db, host=host, user=user
                , passwd=password)

    def close( self ):
        """Close this pygresql connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute_sql( self, sql ):
        self._last_sql = sql
        self._conn.query(sql)

