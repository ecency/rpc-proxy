import functools
import json
import operator
import os
from typing import Dict, Optional

from rpc_proxy.util import file_read

_config: Optional[Dict] = None


def init_config():
    global _config

    this_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    # Todo: Validate config
    path = os.path.join(this_dir, "..", "..", "config.json")

    content = file_read(path)

    _config = json.loads(content)


def config_get(*args):
    if _config is None:
        init_config()

    return functools.reduce(operator.getitem, args, _config)
