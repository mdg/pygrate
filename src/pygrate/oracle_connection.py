import database
import oracle_syntax


class OracleConnection(database.Connection):
    """An oracle database connection wrapper."""

    def __init__( self ):
        database.Connection.__init__( self, oracle_syntax.OracleSyntax() )

    def close( self ):
        pass

    def execute_sql( self, sql ):
        self._last_sql = sql
        # do something

