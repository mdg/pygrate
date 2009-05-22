import pygration
from pygration_set import PygrationSet
from pygration import PygrationType
import os.path
import sys
import imp
import inspect
import types


class Version:
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
        return "<Version(%s)>" % self._string


class PygrationLoader:
    """Loads a given set of Pygrations at runtime."""

    def __init__( self, path, version=None ):
        self._path = path
        self._version = version
        self._modules = []
        self._pygrations = []

    def load( self ):
        self._import_modules()
        self._create_pygrations()
        return self.pygrations()

    def load(self):
        return self._import_module()

    def pygrations( self ):
        return self._pygrations

    def _import_module( self ):
        """Import the module & pygrations for the given version.

        Also creates pygrations from that module and does so in the
        order they are written in the file.
        """

        initial_count = len(PygrationType.pygrations)
        module_name = os.path.join( self._version )
        print "pygration_path = "+ str(module_name)

        sys.path.insert( 0, os.path.abspath( self._path ) )
        mod_trip = imp.find_module(module_name)
        mod = imp.load_module(module_name, *mod_trip)
        self._modules.append( mod )

        pygration_classes = PygrationType.pygrations[initial_count:]
        pygrations = []
        for pcls in pygration_classes:
            pygrations.append( pcls() )
        self._pygrations = pygrations
        return self._pygrations

    def _find_newest_version( self ):
        dirs = os.listdir( self._path )
        newest = None
        for d in dirs:
            v = Version( d )
            if v.is_pygration() and ( (not newest) or cmp(v, newest) > 0 ):
                newest = v
        return newest

    def _find_versions( self ):
        #print "_find_versions"
        files = os.listdir( self._path )
        versions = []
        for f in files:
            p = os.path.join(self._path, f)
            if not os.path.isfile(p):
                continue
            #print "f = %s" % f
            root, ext = os.path.splitext(f)
            if ext != ".py":
                continue
            #print "root, ext = %s, %s" % (root, ext)
            v = Version( root )
            if v.is_pygration():
                versions.append(v)
        versions.sort()
        return versions

