import os
import sys

filepath = os.path.abspath( os.path.dirname( __file__ ) )
parentpath, file = os.path.split( filepath )
sys.path.insert( 0, parentpath )

