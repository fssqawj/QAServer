# coding: utf-8
from similarity import *
from wrapper import timer


@timer
def candidate_sort(p, candidates):
    return sorted(candidates, key=lambda x: similarity(p, x.question), reverse=True)


if __name__ == '__main__':
    pass
