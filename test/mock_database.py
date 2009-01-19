import database


class MockConnection(database.Connection):
    """An mocked version of an actual DB connection."""

    def __init__( self ):
        self._last_sql = ""

    def close( self ):
        pass

    def last_sql( self ):
        return self._last_sql

    def execute_sql( self, sql ):
        self._last_sql = sql

