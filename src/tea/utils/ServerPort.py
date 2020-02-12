# -*- coding: utf-8 -*-

from contextlib import closing
import socket


def find_free_port():
    """
    Get a localhost available port.

    Return:
    -------
        available port of network
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
