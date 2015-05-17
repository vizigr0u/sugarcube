# -*- coding: utf-8 -*-
"""
Sugarcube setuptools setup.py
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sugarcube',
    version='0.1a',
    description='Convert food quantities and units',
    long_description=long_description,
    url='https://github.com/vizigr0u/sugarcube',

    # Author details
    author='Vladimir Nachbaur',
    author_email='vizigr0u@gmail.com',

    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

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
    keywords='cooking units conversion measures',
    py_modules=['sugarcube'],
    install_requires=['future'],
)
