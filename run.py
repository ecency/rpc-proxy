import argparse
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "Requires Python 3.6 or newer"

os.sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        "proxy",
        "test"
    )

    parser.add_argument("cmd", choices=cmd_list, nargs="?", default="proxy")

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == "proxy":
        from rpc_proxy.proxy.app import main
        main()

    if cmd == "test":
        from rpc_proxy.tests import do_tests
        os.environ["TESTING"] = "1"
        do_tests()


if __name__ == '__main__':
    main()
