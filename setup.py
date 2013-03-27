#!/usr/bin/env python

import sys
from distutils.core import setup
from distutils.sysconfig import PREFIX

setup(
    name='port',
    version='0.1',
    description="A ports management tool",
    author="Daniel Walter",
    author_email="d.walter@0x90.at",
    package_dir={'ports':'src/ports'},
    packages=['ports'],
    scripts=['src/port'],
    data_files = [('man/man1',['doc/man/port.1']),
                  ('share/doc/port',['port_complete.csh'])
                 ]
)
