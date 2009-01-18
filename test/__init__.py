import os
import sys

path, file = os.path.split( __file__ )
path, file = os.path.split( path )
sys.path.insert( 0, path )

