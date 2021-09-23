#!/usr/bin/env python3
# coding: utf8

import sys
import os
import socket

from prompt_toolkit.input.vt100 import raw_mode
from prompt_toolkit.input.posix_utils import PosixStdinReader
from utils import readFromWsToFobj, readFromFobjToWs

import asyncio
import websockets


async def newClient(ws, path):

    print("enter newClient")
    with raw_mode(sys.stdin.fileno()):
        print("after setup blocking")
        stdin = os.fdopen(sys.stdin.fileno(), "rb", 0)
        stdout = os.fdopen(sys.stdout.fileno(), "wb", 0)
        tasks = [
            asyncio.create_task(readFromWsToFobj(ws, stdout)),
            asyncio.create_task(readFromFobjToWs(stdin, ws)),
        ]
        done, rest = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

async def main(host, port):

    print("enter main")
    async with websockets.serve(newClient, host, port):
        await asyncio.Future()
	
if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    asyncio.run(main(host, port))
