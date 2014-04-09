#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
      name='ratiofix',
      version='1.0',
      author='Jared Miller',
      author_email='jared@cantcode.com',
      description='Stupid attempt at fixing a what.cd ratio.',
      license='BSD',
      url='https://github.com/shmup/ratiofix',
      install_requires=(
        'pyquery',
        'requests'
        )
     )
