#!/usr/bin/env python3
"""
A web go server.

"""
import argparse

import modules.match_manager as match_manager
import modules.webserver as webserver


def parse_commandline():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--port',
        help='Port on which the server will be opened', default=5000, type=int
    )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_commandline()

    # init the match manager
    match_manager.init()

    go_server = webserver.WebServer(args.port)
    go_server.start()
