import re
import hashlib
from typing import List, Optional


def route_match(routes: List[str], path: str) -> Optional[str]:
    match = [x for x in routes if re.compile(x).match(path)]

    if len(match) == 0:
        return None

    return match[0]

def gen_etag(content):
    """generate an Etag for the response"""
    etag = hashlib.sha256() # sha256
    etag.update(content.encode("utf-8")) # create an etag
    etag.hexdigest() # to hexadecimal format
    return etag