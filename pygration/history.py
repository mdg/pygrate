import sqlalchemy
from sqlalchemy import Column, Integer, String
from pygration.db import PygrationState, Table


class History:
    """A class for loading version history from the DB.  It also writes
    history back to the DB as it changes."""

    def __init__(self, session):
        self._session = session

    def committed(self, version):
        return False

    def load(self):
        self._history = self._session.query(PygrationState).all()

    def state(self, version, step):
        for state in self._history:
            if version == state.migration and step == state.step:
                return state
        return PygrationState(version, step)

    def store(self, version, step, state):
        pass

    def versions(self):
        return []


def load(session):
    create_failed = False

    try:
        print "\n...\tcreating version_state table"
        Table.pygration_state.create()
        session.commit()
    except:
        create_failed = True
        print "error creating table.  assume it already exists and continue."

    h = History(session)
    try:
        h.load()
    except Exception, x:
        print "error loading version history"
        if create_failed:
            print "create version_state table failed"
        else:
            print "create version_state table succeeded"
        raise x
    return h

