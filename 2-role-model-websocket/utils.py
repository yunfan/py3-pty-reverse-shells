#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import asyncio

class nonblocking(object):
    """
    Make fd non blocking.
    copy from pymux.utils
    """
    def __init__(self, fd):
        self.fd = fd

    def __enter__(self):
        import fcntl
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

    def __exit__(self, *args):
        import fcntl
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

async def readFromWsToFobj(ws, fobj, debug=False):
    async for msg in ws:
        if debug:
            print(msg, type(msg), len(msg))
        fobj.write(msg)

async def readFromFobjToWs(fobj, ws):
    while True:
        with nonblocking(fobj.fileno()):
            try:
                data = fobj.read(1024)
                if data is None or not data:
                    await asyncio.sleep(0.01)
                    continue
                await ws.send(data)
            except EOFError:
                await asyncio.sleep(0.01)
                continue
