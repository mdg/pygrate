import os
import os.path
import imp
import sys



class Step(object):
    """Static class for defining migration steps"""
    steps = []

    @staticmethod
    def step_class(cls):
        print "step: %s.%s" % (cls.__module__, cls.__name__)
        cls.version = cls.__module__
        cls.step_name = cls.__name__
        cls.step_id = cls.step_name
        Step.steps.append(cls())
        return cls

    @staticmethod
    def step_instance(step):
        print "step: %s.%s" % (step.__class__.__module__
                , step.__class__.__name__)
        step.version = step.__class__.__module__
        if getattr(step, 'step_name', None) is None:
            step.step_name = step.__class__.__name__
        step.step_id = step.step_name
        Step.steps.append(step)

    @staticmethod
    def extract_steps():
        extraction = Step.steps
        Step.steps = []
        return extraction


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
        #print "compare %s to %s = %d" % (component1, component2, comparison)
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

    def __str__(self):
        return self._string

    def __repr__(self):
        return "<VersionNumber(%s)>" % self._string


class Migration(object):
    """A logical set of changes to the database.

    Named by a version number.
    """
    def __init__(self, version, steps=[]):
        self._version = version
        self._steps = steps

    def version(self):
        return self._version

    def steps(self):
        return self._steps

    def step(self, index):
        return self._steps[index]

    def __repr__(self):
        return "<Migration(%s)>" % (self._version)


class MigrationSet(object):
    """An object for holding the set of available migrations."""

    def __init__(self, migs):
        self._migrations = migs
        self._find_versions()

    def versions(self):
        return self._versions

    def migrations(self):
        return self._migrations

    def migration(self, version):
        """Get the migration module for a given version."""
        if version in self._migrations:
            return version # self._migrations[version]
        return None

    def steps(self, migration):
        return []

    def _find_versions(self):
        self._versions = set()
        for m in self._migrations:
            self._versions.add(m.version())

    def ordered_migrations(self):
        for m in sorted(self._migrations, key=lambda m: m.version()):
            yield m


class Loader(object):
    """Object for finding available MigrationSets."""

    def __init__(self, path):
        self._path = path
        self._files = None
        self._versions = None
        self._modules = []
        self._set = None
        self._migrations = []

    def load(self):
        """Load migration modules from the given path."""
        if self._set is None:
            self._find_files()
            self._find_versions()
            self._load_migrations()
            self._set = MigrationSet(self._migrations)
        return self._set

    def _find_files(self):
        """Find python files at the given path."""
        self._files = []
        entries = os.listdir(self._path)
        for e in entries:
            p = os.path.join(self._path, e)
            if os.path.isfile(p) and p.endswith('.py'):
                self._files.append(p)

    def _find_versions(self):
        """Find version numbers based on a given set of files."""
        self._versions = []
        for f in self._files:
            filename = os.path.basename(f)
            root, ext = os.path.splitext(filename)
            v = VersionNumber(root)
            if v.is_pygration():
                self._versions.append(v)
        self._versions.sort()
        return self._versions

    def _load_migrations(self):
        self._modules = []
        self._migrations = []
        for v in self._versions:
            self._load_migration_module(str(v))

    def _set_import_path(self):
        abspath = os.path.abspath(self._path)
        if abspath not in sys.path:
            # Add the path to the sys.path
            sys.path.insert(0, abspath)

    def _load_migration_module(self, module_name):
        # print "load module(%s)" % module_name
        self._set_import_path()
        mod_trip = imp.find_module(module_name)
        mod = imp.load_module(module_name, *mod_trip)
        self._modules.append(mod)
        steps = Step.extract_steps()
        for s in steps:
            print "\t%s" % (s.step_name)
        m = Migration(module_name, steps)
        self._migrations.append(m)
        print "remaining steps:\n\t", Step.steps


def load(path):
    m = Loader(path)
    return m.load()

