

class History:
    """A class for loading version history from the DB.  It also writes
    history back to the DB as it changes."""

    def __init__(self, schema, dbconn):
        self._schema = schema
        self._db = dbconn

    def load(self):
        pass

    def store(self, version_set):
        pass

    def versions(self):
        return []

