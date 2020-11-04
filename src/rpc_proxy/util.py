import os
from typing import Any, Union


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


def assert_env_vars(*args) -> Union[list, str]:
    li = []

    for a in args:
        v = os.environ.get(a)

        if v is None:
            raise AssertionError('{} environment variable required'.format(a))

        li.append(v)

    return li[0] if len(li) == 1 else li
