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
    #h = History(schema)
    h = []
    retry = False
    try:
        h = session.query(VersionState).all()
    except sqlalchemy.exc.ProgrammingError, saerr:
        token = '.version_state" does not exist\n'
        if str(saerr.args[0]).endswith(token):
            retry = True
        else:
            raise saerr

    if retry:
        Table.version_state.create()
        session.commit()
        h = session.query(VersionState).all()
    return h

