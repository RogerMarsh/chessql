# setup.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='chessql',
        version='1.2',
        description='Chess Query Language (cql) parser',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        packages=[
            'chessql',
            'chessql.core',
            'chessql.core.test',
            ],
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Operating System :: OS Independent',
            'Topic :: Software Development',
            'Topic :: Games/Entertainment :: Board Games',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta',
            ],
        install_requires=[
            'pgn-read==1.3',
            ],
        dependency_links=[
            'http://solentware.co.uk/files/pgn-read-1.3.tar.gz',
            ],
        )
