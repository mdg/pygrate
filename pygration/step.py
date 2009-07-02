
# forward declaration only.  redefined below.
def pygration_step_subclass(cls):
    pass


class StepType(type):
    pygrations = []

    def __init__(cls, name, bases, cls_dict):
        super(StepType, cls).__init__(name, bases, cls_dict)
        if not pygration_step_subclass(cls):
            return
        cls.pygrations.append(cls)


class Step(object):
    """A single logical change to the database.

    The Step is composed of multiple Phases to make changes prior to and
    subsequent to the application deployment.
    """

    __metaclass__ = StepType

    def __init__( self ):
        self._failure = False

    def pre_add_check( self, db ):
        """Validate the DB is in the expected state prior to the add."""
        # p = PreAddCheckPygrationDB(db)
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
        p = CommitPygrationDB(db)
        self.drop(p)

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        p = RollbackPygrationDB(db)
        self.add(p)

    def rollback_drop( self, db ):
        """Rollback any items that were hidden in the db"""
        p = RollbackPygrationDB(db)
        self.add(p)

    def failure( self ):
        return self._failure

    def _fail( self, msg ):
        self._failure = msg


class VersionNumber:
    def __init__( self, ver_string ):
        self._parse_version( ver_string )

    def is_pygration(self):
        return self._is_pygration

    def __cmp__(self, other):
        """Compare 2 versions to see which is earlier."""
        if not other:
            return -1

        if (not (self.is_pygration() or other.is_pygration() )):
            return 0
        if (self.is_pygration() and not other.is_pygration()):
            return -1
        if (other.is_pygration() and not self.is_pygration()):
            return 1

        i = 0
        while i<len(self._array) and i<len(other._array):
            comparison = self._component_compare( self._array[i]
                    , other._array[i])
            if comparison != 0:
                return comparison

            i = i + 1

        if len(self._array) < len(other._array):
            return -1
        if len(self._array) > len(other._array):
            return 1

        return 0

    def _component_compare(self,component1,component2):
        """Compare 2 components of a version."""
        try:
            number1 = int(component1)
            number2 = int(component2)
            component1, component2 = number1, number2
        except:
            pass
        comparison = 0
        if component1 < component2:
            comparison = -1
        if component1 > component2:
            comparison = 1
        print "compare %s to %s = %d" % (component1, component2, comparison)
        return comparison

    def _component(self,index):
        return self._array[index]

    def _parse_version( self, ver_string ):
        self._is_pygration = False
        self._string = ""
        self._array = []

        if ver_string[0] != 'v':
            return

        array = [ ver_string[1:] ]
        seps = ['-','_','.']
        i=0
        for s in seps:
            tmp_array = []
            for c in array:
                tmp_array.extend(c.split(s))
            array = tmp_array

        self._is_pygration = True
        self._string = ver_string
        self._array = array

    def __repr__(self):
        return "<VersionNumber(%s)>" % self._string


class VersionSet(object):
    """A logical set of changes to the database.

    Named by a version number.
    """
    pass


def pygration_step_subclass(cls):
    if not isinstance(cls, type):
        return False
    # print "%s.name = '%s'" % (cls, cls.__name__)
    return issubclass(cls, Step) and cls != Step

