import functools
import json
import operator
import os

from rpc_proxy.logger import create_logger
from rpc_proxy.util import file_read

logger = create_logger('config')

_config = None


def make_config():
    global _config

    this_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    # Todo: Validate config
    path = os.path.join(this_dir, "..", "..", "config.json")

    content = file_read(path)

    _config = json.loads(content)


make_config()


def config_get(*args):
    return functools.reduce(operator.getitem, args, _config)
