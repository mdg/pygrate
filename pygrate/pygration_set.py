import pygration


class PygrationSet(pygration.Pygration):
    """A collection of steps to change the database.
    
    The pygration includes steps to make the change prior to and
    subsequent to the application deployment.
    """

    def __init__( self, pygrations ):
        self._pygrations = pygrations
        self._function = { "add": self.add, "hide": self.hide
                , "drop": self.drop }

    def migrate( self, db, stage ):
        f = self._function[stage]
        f( db )

    def add( self, db ):
        """Add elements to the db"""
        for p in self._pygrations:
            p.add( db )

    def hide( self, db ):
        """Hide elements in the db before dropping them"""
        for p in self._pygrations:
            p.hide( db )

    def drop( self, db ):
        """Permanently drop elements from the db"""
        for p in self._pygrations:
            p.drop( db )

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        for p in self._pygrations:
            p.rollback_add( db )

    def rollback_hide( self, db ):
        """Rollback any items that were hidden in the db"""
        for p in self._pygrations:
            p.rollback_hide( db )

