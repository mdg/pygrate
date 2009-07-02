

class VersionState:
    """A class for loading version state from the DB."""
    def __init__(self, db_conn):
        self._db = db_conn

    def load(self):
        pass

    def store(self, version_set):
        pass

    def latest_version(self):
        pass

