import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "rpc_proxy requires Python 3.6 or newer"

setup(
    name='rpc_proxy',
    version='0.0.9',
    description='rpc proxy',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        'sanic==20.12.4',
        'sanic_cors==0.10.0.post3',
        'websockets==8.1',
        'requests==2.26.0',
        'aiocache==0.11.1',
        'aioredis>=1,<2'
    ],
    entry_points={
        'console_scripts': [
            'rpc_proxy=run:main'
        ]
    })
