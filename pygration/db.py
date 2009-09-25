import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker


class PygrationState(object):
    def __init__(self, migration=None, step_id=None, step_name=None):
        self.migration = migration
        self.step_id = step_id
        self.step_name = step_name
        self.sequence = None
        self.add_state = None
        self.simdrop_state = None
        self.drop_state = None

    def __repr__(self):
        return "<PygrationState(%s, %s)>" % (self.migration, self.step_id)


class Table(object):
    metadata = sqlalchemy.MetaData()
    engine = None

    pygration_state = None

    @classmethod
    def define(cls, schema=None):
        cls.pygration_state = sqlalchemy.Table('pygration_state', cls.metadata
                , Column('migration', String, primary_key=True)
                , Column('step_id', String(length=40), primary_key=True)
                , Column('step_name', String(length=80))
                , Column('sequence', Integer)
                , Column('add_state', String(length=16))
                , Column('simdrop_state', String(length=16))
                , Column('drop_state', String(length=16))
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

