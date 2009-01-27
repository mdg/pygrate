import pygration
import os.path
import sys
import inspect
import types


class Version:
    def __init__( self, ver_string ):
        self._parse_version( ver_string )

    def is_pygration(self):
        return self._is_pygration

    def compare(self, other):
        """Compare 2 versions to see which is earlier."""
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


class PygrationLoader:
    """Loads a given set of Pygrations at runtime."""

    def __init__( self, path, version ):
        self._path = path
        self._version = version
        self._modules = []
        self._pygrations = []
        if not self._version:
            self._version = self._find_version()

    def load( self ):
        self._import_modules()
        self._create_pygrations()
        return self.pygrations()

    def pygrations( self ):
        return self._pygrations

    def _import_modules( self ):
        module_names = self._list_modules()
        modules = []
        sys.path.insert( 0, os.path.abspath( self._path ) )
        for n in module_names:
            # should filter these files somehow
            import_path = os.path.join( self._version, n )
            # print "__import__( "+ import_path +")"
            mod = __import__( import_path )
            modules.append( mod )
        self._modules.extend( modules )

        # mod_name = os.path.join( self._path, self._migration )
        # print "mod_name = "+ str(mod_name)
        # mod = __import__( mod_name )
        # print str(dir(mod))

    def _create_pygrations( self ):
        pygs = []
        for mod in self._modules:
            # print "module: "+ str(mod) + "\n"
            for pyg in mod.__dict__.values():
                if self._pygration_subclass(pyg):
                    # print "mig: "+ str(pyg.__name__)
                    pygs.append(pyg())
        self._pygrations.extend( pygs )

    def _list_modules( self ):
        pygration_path = os.path.join( self._path, self._version )
        print "pygration_path = "+ str(pygration_path)
        files = os.listdir( pygration_path )
        pygrations = []
        for f in files:
            if f.endswith( '.py' ):
                pygrations.append( f.replace( ".py", "" ) )
        return pygrations

    def _find_version( self, version ):
        return version

    def _pygration_subclass( self, obj ):
        if type(obj) is not types.ClassType:
            return False
        return issubclass(obj, pygration.Pygration) \
                and not obj == pygration.Pygration

