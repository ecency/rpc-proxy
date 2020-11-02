import os
from typing import Any


def file_write(path: str, data: Any, mode: str = 'w'):
    with open(path, mode) as f:
        f.write(data)
        f.close()


def file_read(path: str, mode='r') -> Any:
    with open(path, mode) as f:
        output = f.read()
        f.close()

    return output


def file_delete(path: str):
    os.unlink(path)
