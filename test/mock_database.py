import database


class MockConnection(database.Connection):
    """An mocked version of an actual DB connection."""

    def __init__( self, syntax ):
        database.Connection.__init__( self, syntax )
        self._last_sql = ""

    def close( self ):
        pass

    def last_sql( self ):
        return self._last_sql

    def execute_sql( self, sql ):
        self._last_sql = sql

