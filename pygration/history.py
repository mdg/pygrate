import sqlalchemy
from sqlalchemy import Column, Integer, String


class History:
    """A class for loading version history from the DB.  It also writes
    history back to the DB as it changes."""

    metadata = sqlalchemy.MetaData()
    version_history_table = sqlalchemy.Table('version_history', metadata
            , Column('version_number', String, primary_key=True)
            , Column('sequence', Integer)
            , Column('add', String)
            , Column('drop', String)
            , Column('commit', String)
            )

    def __init__(self, engine, schema=None):
        self._engine = engine
        self._schema = schema

    def load(self):
        pass

    def store(self, version_set):
        pass

    def versions(self):
        return []

def load(dbconn, schema=None):
    h = History(dbconn, schema)
    h.load()
    return h

