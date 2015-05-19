# -*- coding: utf-8 -*-
"""
Sugarcube setuptools setup.py
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

ProjectName = 'sugarcube'
ProjectVersion = '0.1b'

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=ProjectName,
    version=ProjectVersion,
    description='Convert food quantities and units',
    long_description=long_description,
    keywords='cooking units conversion measures',

    # Author details
    author='Vladimir Nachbaur',
    author_email='vizigr0u@gmail.com',
    url='https://github.com/vizigr0u/' + ProjectName,

    install_requires=['future'],
    py_modules=[ProjectName],

    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
