#! /usr/bin/python

import pygrate.loader
import pygrate.database
import pygrate.pygrator
from pygrate.pygration_set import PygrationSet
import optparse
import os.path
import sys
import types


def run_main():
    usage = "usage: %prog [options] operation migration"
    parser = optparse.OptionParser( usage=usage )
    parser.add_option( "-p", "--path" )

    opts, args = parser.parse_args()

    if len(args) == 0:
        parser.error("A stage must be specified")
    if len(args) == 1:
        parser.error("A migration set must be specified")
    if len(args) > 2:
        parser.error("Too many arguments")

    operation = args[0]
    migration = args[1]

    path = '.'
    if opts.path:
        print "opts.path="+ opts.path
        path = opts.path

    db = pygrate.database.open( path )

    loader = pygrate.loader.PygrationLoader( path, migration )
    loader.load()

    set = PygrationSet( loader.pygrations() )
    p = pygrate.pygrator.Pygrator( db )
    set.migrate( p, operation )

    db.close()


if ( __name__ == "__main__" ):
    run_main()

