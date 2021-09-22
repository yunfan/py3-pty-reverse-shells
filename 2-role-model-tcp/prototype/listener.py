#!/usr/bin/env python3
# coding: utf8

import sys
import socket
import select

from prompt_toolkit.input.vt100 import raw_mode
from utils import SelectableJointPool 


class Shell:
    def __init__(self, host, port):
        self.addr = (host, port)

        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(5)

    def handle(self):
        sock, addr = self.sock.accept()

        pool = SelectableJointPool()
        pool.join(sys.stdin.fileno(), sock.fileno())
        pool.join(sock.fileno(), sys.stdout.fileno())

        while True:
            pool.run()

        # close the socket
        sock.close()

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = Shell(host, port)
    with raw_mode(sys.stdin.fileno()):
        s.handle()
