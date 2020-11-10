import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 5, "rpc_proxy requires Python 3.6 or newer"

setup(
    name='rpc_proxy',
    version='0.0.5',
    description='rpc proxy',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        'sanic',
        'sanic_cors',
        'websockets',
        'requests',
        'aiocache',
        'aioredis'
    ],
    entry_points={
        'console_scripts': [
            'rpc_proxy=run:main'
        ]
    })
