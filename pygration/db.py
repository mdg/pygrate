import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker


class PygrationState(object):
    def __init__(self, migration=None):
        self.migration = migration
        self.step = None
        self.sequence = None
        self.add = None
        self.drop = None
        self.commit = None

    def __repr__(self):
        return "<PygrationState(%s)>" % (self.migration)


class Table(object):
    metadata = sqlalchemy.MetaData()
    engine = None

    pygration_state = None

    @classmethod
    def define(cls, schema=None):
        cls.pygration_state = sqlalchemy.Table('pygration_state', cls.metadata
                , Column('migration', String, primary_key=True)
                , Column('step', String, primary_key=True)
                , Column('sequence', Integer)
                , Column('add', String)
                , Column('drop', String)
                , Column('commit', String)
                , schema=schema
                )


def open(connection, schema=None):
    """Open the DB through a SQLAlchemy engine.
 
    Returns an open session.
    """
    Table.engine = sqlalchemy.create_engine(connection)
    Table.metadata.bind = Table.engine

    Session = sessionmaker()
    Session.configure(bind=Table.engine)
    session = Session()

    Table.define(schema)
    mapper(PygrationState, Table.pygration_state)
    return session

