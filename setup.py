#!/usr/bin/env python

from distutils.core import setup

setup(name='pygrate',
        version='0.2',
        description='Python DB Migration Framework',
        author='Matthew Graham',
        url='http://github.com/mdg/pygrate',
        scripts=['bin/pygrate'],
        packages=['pygration']
        )

