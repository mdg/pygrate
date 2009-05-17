

class Pygration:
    """A collection of steps to change the database.
    
    The pygration includes steps to make the change prior to and
    subsequent to the application deployment.
    """

    def __init__( self ):
        self._failure = False

    def pre_add_check( self, db ):
        """Validate the DB is in the expected state prior to the add."""
        # p = PreAddCheckPygrator(db)
        # self.add(p)
        # do nothing for now.  get actual behavior right first.
        pass

    def post_add_check( self, db ):
        """Validate the DB is in the expected state after the add."""
        pass

    def add( self, db ):
        """Add elements to the db"""
        pass

    def drop( self, db ):
        """Hide elements in the db before dropping them"""
        pass

    def commit_drop( self, db ):
        """Permanently drop elements from the db"""
        p = CommitPygrator(db)
        self.drop(p)

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        p = RollbackPygrator(db)
        self.add(p)

    def rollback_drop( self, db ):
        """Rollback any items that were hidden in the db"""
        p = RollbackPygrator(db)
        self.add(p)

    def failure( self ):
        return self._failure

    def _fail( self, msg ):
        self._failure = msg


class Column:
    def __init__( self, type, name, size=None ):
        self._type = type
        self._name = name
        self._size = size

    def type( self ):
        return self._type

    def name( self ):
        return self._name

    def postgres_type( self ):
        return self._type

    def oracle_type( self ):
        return self._type

class String(Column):
    """The string type for pygration table columns."""

    DEFAULT_SIZE = 40

    def __init__( self, name, size=None ):
        if not size:
            size = String.DEFAULT_SIZE
        Column.__init__( self, "string", name, size )

    def postgres_type( self ):
        return "varchar(%d)" % ( self._size )

    def oracle_type( self ):
        return "varchar2(%d)" % ( self._size )

class Number(Column):
    def __init__( self, name ):
        Column.__init__( self, "number", name )


class Table:
    def __init__(self, name, columns):
        self._name = name
        self._columns = columns

    def name(self):
        """Get the name of this table."""
        return self._name

    def num_columns(self):
        """Get the number of columns in this table."""
        return len(self._columns)

    def column(self,idx):
        """Get a specific column in this table."""
        return self._columns[idx]

    def columns(self):
        return iter(self._columns)

