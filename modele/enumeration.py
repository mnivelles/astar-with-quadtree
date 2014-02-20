#!/usr/bin/env python
# -*- coding: utf-8 -*-

# source : http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)