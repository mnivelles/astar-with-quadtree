#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, autre):
        return (self.x, self.y) == (autre.x, autre.y)

    def __str__(self):
        return "p(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "p(" + str(self.x) + ", " + str(self.y) + ")"