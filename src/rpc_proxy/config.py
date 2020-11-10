import functools
import json
import operator
import os
from typing import Dict, Optional

from rpc_proxy.util import file_read

_config: Optional[Dict] = None


class NoSuchConfigException(BaseException):
    pass


def init_config(config_path):
    global _config

    if not os.path.isfile(config_path):
        print("Config file not found at path: {}".format(config_path))
        exit(1)

    content = file_read(config_path)

    _config = json.loads(content)


def config_get(*args):
    try:
        return functools.reduce(operator.getitem, args, _config)
    except KeyError:
        j_args = ".".join(args)
        raise NoSuchConfigException("No such config: {}".format(j_args))


def config_get_timeout(target_name: str):
    timeouts = config_get("timeouts")

    if isinstance(timeouts, int):
        return timeouts
    else:
        return config_get("timeouts", target_name)
