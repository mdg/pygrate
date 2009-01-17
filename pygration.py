

class Pygration:
    """A collection of steps to change the database.
    
    The pygration includes steps to make the change prior to and
    subsequent to the application deployment.
    """

    def __init__( self ):
        pass

    def add( self, db ):
        """Add elements to the db"""
        pass

    def hide( self, db ):
        """Hide elements in the db before dropping them"""
        pass

    def drop( self, db ):
        """Permanently drop elements from the db"""
        pass

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        pass

    def rollback_hide( self, db ):
        """Rollback any items that were hidden in the db"""
        pass

