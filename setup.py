#!/usr/bin/env python

from distutils.core import setup

setup(name='pygrate',
        version='1.0',
        description='Python DB Migration Framework',
        author='Matthew Graham',
        url='http://github.com/mdg/pygrate',
        scripts=['bin/pygrate'],
        packages=['pygrate'],
        package_dir={'pygrate': 'src/pygrate'}
        )

