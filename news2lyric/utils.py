# -*- coding: utf-8 -*-


def combinations(*args):
    if len(args) == 1:
        return [[x] for x in args[0]]
    combs = []
    for item in args[0]:
        for x in combinations(*args[1:]):
            combs.append([item] + x)
    return combs


def flatten(l):
    return [item for sublist in l for item in sublist]