import sqlalchemy
from sqlalchemy import Column, Integer, String
from pygration.db import PygrationState, Table


class History:
    """A class for loading version history from the DB.  It also writes
    history back to the DB as it changes."""

    def __init__(self, history):
        self._history = history

    def committed(self, version):
        return False

    def state(self, version, stepid, stepname):
        for state in self._history:
            if version == state.migration and stepid == state.step_id:
                return state
        return PygrationState(version, stepid, stepname)

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

    try:
        rows = session.query(PygrationState).all()
        h = History(rows)
    except Exception, x:
        print "error loading version history"
        if create_failed:
            print "create version_state table failed"
        else:
            print "create version_state table succeeded"
        raise x
    return h

