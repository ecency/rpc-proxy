import argparse
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "Requires Python 3.6 or newer"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))


def main():
    parser = argparse.ArgumentParser(description='')
    cmd_list = (
        "proxy",
        "test"
    )

    parser.add_argument("cmd", choices=cmd_list, nargs="?", default="proxy")
    parser.add_argument("--config", dest="config")

    args = parser.parse_args()
    cmd = args.cmd

    if cmd == "proxy":
        config = args.config

        if config is None:
            print("--config parameter required!")
            exit(1)

        from rpc_proxy.config import init_config
        from rpc_proxy.app import main

        init_config(args.config)

        main()

    if cmd == "test":
        from rpc_proxy.tests import do_tests
        os.environ["TESTING"] = "1"
        do_tests()


if __name__ == '__main__':
    main()
