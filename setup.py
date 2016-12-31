# Copyright (c) Jack Grigg
# See LICENSE for details.

from setuptools import setup


setup(
    name='videonion',
    version='0.0.1',
    description='Bi-directional point-to-point video streaming over a hidden service',
    url='https://github.com/alecmuffett/videonion',

    install_requires=[
        'magic-wormhole',
    ],
    packages=[
        'videonion',
    ],
    entry_points={
        'console_scripts':
        [
            'videonion = videonion.cli:videonion',
        ]
    },
)
