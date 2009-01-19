import pygration
import os.path
import sys
import inspect
import types


class PygrationLoader:
    """Loads a given set of Pygrations at runtime."""

    def __init__( self, path, pygration_set ):
        self._path = path
        self._pygration_set = pygration_set
        self._modules = []
        self._pygrations = []

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
            import_path = os.path.join( self._pygration_set, n )
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
        pygration_path = os.path.join( self._path, self._pygration_set )
        print "pygration_path = "+ str(pygration_path)
        files = os.listdir( pygration_path )
        pygrations = []
        for f in files:
            if f.endswith( '.py' ):
                pygrations.append( f.replace( ".py", "" ) )
        return pygrations

    def _pygration_subclass( self, obj ):
        if type(obj) is not types.ClassType:
            return False
        return issubclass(obj, pygration.Pygration) \
                and not obj == pygration.Pygration

