

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
        return "text"

    def oracle_type( self ):
        return "varchar2(%d)" % ( self._size )

class Number(Column):
    def __init__( self, name ):
        Column.__init__( self, "number", name )

class Integer(Column):
    def __init__( self, name ):
        Column.__init__( self, "integer", name )


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

