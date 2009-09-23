
# forward declaration only.  redefined below.
def pygration_step_subclass(cls):
    pass


class StepType(type):
    steps = []

    def __init__(cls, name, bases, cls_dict):
        super(StepType, cls).__init__(name, bases, cls_dict)
        if not pygration_step_subclass(cls):
            return
        StepType.steps.append(cls)

    @staticmethod
    def extract_steps():
        extract = StepType.steps
        StepType.steps = []
        return extract


class Step(object):
    """A single logical change to the database.

    The Step is composed of multiple Phases to make changes prior to and
    subsequent to the application deployment.
    """

    __metaclass__ = StepType

    def __init__( self ):
        self._failure = False

    @classmethod
    def step_id(cls):
        if hasattr(cls, "ID"):
            return getattr(cls, "ID")
        return cls.step_name()

    @classmethod
    def step_name(cls):
        return cls.__name__

    def pre_add_check( self, db ):
        """Validate the DB is in the expected state prior to the add."""
        # p = PreAddCheckPygrationDB(db)
        # self.add(p)
        # do nothing for now.  get actual behavior right first.
        return True

    def post_add_check( self, db ):
        """Validate the DB is in the expected state after the add."""
        return True

    def add( self, db ):
        """Add elements to the db"""
        pass

    def drop( self, db ):
        """Hide elements in the db before dropping them"""
        pass

    def commit_drop( self, db ):
        """Permanently drop elements from the db"""
        pass

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        pass

    def rollback_drop( self, db ):
        """Rollback any items that were hidden in the db"""
        pass

    def failure( self ):
        return self._failure

    def _fail( self, msg ):
        self._failure = msg


def pygration_step_subclass(cls):
    if not isinstance(cls, type):
        return False
    # print "%s.name = '%s'" % (cls, cls.__name__)
    return issubclass(cls, Step) and cls != Step

