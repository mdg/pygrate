import sqlalchemy
from sqlalchemy import Column, Integer, String
from pygration.db import VersionState, Table


class History:
    """A class for loading version history from the DB.  It also writes
    history back to the DB as it changes."""

    def __init__(self, schema=None):
        self._schema = schema

    def load(self):
        History.metadata.version_history_table.query()
        pass

    def store(self, version_set):
        pass

    def versions(self):
        return []


def load(session):
    create_failed = False

    try:
        print "\n...\tcreating version_state table"
        Table.version_state.create()
        session.commit()
    except:
        create_failed = True
        print "error creating table.  assume it already exists and continue."

    h = None
    try:
        h = session.query(VersionState).all()
    except Exception, x:
        print "error querying version history"
        if create_failed:
            print "create version_state table failed"
        else:
            print "create version_state table succeeded"
        raise x
    return h

