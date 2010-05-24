import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
import subprocess

class PygrationState(object):
    '''Python object representing the state table'''
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
                , Column('migration', String(length=160), primary_key=True)
                , Column('step_id', String(length=160), primary_key=True)
                , Column('step_name', String(length=160))
                , Column('sequence', Integer)
                , Column('add_state', String(length=16))
                , Column('simdrop_state', String(length=16))
                , Column('drop_state', String(length=16))
                , schema=schema
                )

class FileLoader(object):
    '''Object for running SQL from a file on the file system'''
    def __init__(self, binary, args = [], formatting_dict = {}):
        self._binary = binary
        self._args = [arg.format(filename="{filename}", **formatting_dict) for arg in args]
    
    def __call__(self, filename):
        args = [arg.format(filename=filename) for arg in self._args]
        print self._binary, args
        subprocess.check_call([self._binary] + args)


def open(url=None, drivername=None, schema=None, username=None,
         password=None, host=None, port=None, database=None, query=None):
    """Open the DB through a SQLAlchemy engine.
 
    Returns an open session.
    """
    
    if url is None and drivername is None:
        raise Exception("Either a url or a driver name is required to open a db connection")

    if url is None:
        url = sqlalchemy.engine.url.URL(drivername = drivername,
                                        username = username,
                                        password = password,
                                        host = host,
                                        port = port,
                                        database = database,
                                        query = query)

    Table.engine = sqlalchemy.create_engine(url)
    Table.metadata.bind = Table.engine

    Session = sessionmaker()
    Session.configure(bind=Table.engine)
    session = Session()

    Table.define(schema)
    mapper(PygrationState, Table.pygration_state)
    return session

