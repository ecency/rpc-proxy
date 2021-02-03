import re
from typing import List, Optional

from rpc_proxy.util import md5


def route_match(routes: List[str], path: str) -> Optional[str]:
    match = [x for x in routes if re.compile(x).match(path)]

    if len(match) == 0:
        return None

    return match[0]


def gen_etag(content):
    return md5(content)
