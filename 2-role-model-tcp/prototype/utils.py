#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import select
import queue

class SelectableJointPool(object):
    def __init__(self):
        self.pipes = {}
        self.buffers = {}   ## buffers of to write
        self.readList = []
        self.writeList = []
        self.bufsize = 1024

    def join(self, rfd, wfd):

        if rfd in self.pipes:
            raise Exception(f"rfd had already joined")

        os.set_blocking(rfd, False)
        os.set_blocking(wfd, False)

        self.pipes[rfd] = wfd
        self.buffers[wfd] = queue.Queue()

        self.readList.append(rfd)
        self.writeList.append(wfd)

    def step(self):
        readable, writable, _ = select.select(self.readList, self.writeList, [])

        for srcfd in readable:
            buf = os.read(srcfd, self.bufsize)
            self.buffers[self.pipes[srcfd]].put(buf)

        for dstfd in writable:
            dstBuffer = self.buffers[dstfd]
            if dstBuffer.empty(): continue
            os.write(dstfd, dstBuffer.get())

    def run(self, counts=-1):
        step = 0
        while step != counts:
            step += 1
            self.step()
