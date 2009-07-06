import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker


class VersionState(object):
    def __init__(self):
        self.version_number = None
        self.sequence = None
        self.add = None
        self.drop = None
        self.commit = None


class Table(object):
    metadata = sqlalchemy.MetaData()
    engine = None

    version_state = None

    @classmethod
    def define(cls, schema=None):
        cls.version_state = sqlalchemy.Table('version_state', cls.metadata
                , Column('version_number', String, primary_key=True)
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
    mapper(VersionState, Table.version_state)
    return session

